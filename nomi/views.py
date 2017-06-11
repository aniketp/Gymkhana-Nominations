from django.shortcuts import render
from forms.models import Question
from .models import Nomination, NominationInstance, UserProfile, Post, Club
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from .forms import NominationForm, PostForm, ConfirmApplication, ClubForm
from forms.models import Questionnaire
import json


@login_required
def index(request):
    nominations = Nomination.objects.filter(status='Nomination out')
    all_nominations = nominations[::-1]
    posts = Post.objects.filter(post_holders=request.user)
    clubs = Club.objects.filter(club_members=request.user)
    username = UserProfile.objects.get(user=request.user)

    return render(request, 'index.html', context={'all_nominations': all_nominations, 'posts': posts,
                                                  'clubs': clubs, 'username': username})


@login_required
def club_list(request):
    admin_club = Club.objects.get(club_name="Admin")
    clubs = Club.objects.filter(club_parent=admin_club)

    return render(request, 'clubs/council_clubs.html', context={'clubs': clubs})


@login_required
def club_view(request, pk):
    club = Club.objects.get(pk=pk)
    child_clubs = Club.objects.filter(club_parent=club)
    child_clubs_reverse = child_clubs[::-1]
    posts = Post.objects.filter(post_holders=request.user)

    club_approvals = Club.objects.filter(club_approvals=club).filter(status='Club created')

    return render(request, 'club.html', context={'club': club, 'child_clubs': child_clubs_reverse,
                                                 'posts': posts, 'club_approval': club_approvals})


@login_required
def post_view(request, pk):
    post = Post.objects.get(pk=pk)
    child_posts = Post.objects.filter(parent=post)
    child_posts_reverse = child_posts[::-1]

    post_approvals = Post.objects.filter(post_approvals=post).filter(status='Post created')
    nomi_approvals = Nomination.objects.filter(nomi_approvals=post).filter(status='Nomination created')

    if request.user in post.post_holders.all():
        return render(request, 'post.html', context={'post': post, 'child_posts': child_posts_reverse,
                                                     'post_approval': post_approvals, 'nomi_approval': nomi_approvals})
    else:
        return render(request, 'no_access.html')


@login_required
def club_create(request, pk):
    if request.method == 'POST':
        parent = Club.objects.get(pk=pk)
        club_form = ClubForm(request.POST)

        if club_form.is_valid():
            club = Club.objects.create(club_name=club_form.cleaned_data['club_name'], club_parent=parent)
            club_pk = club.pk

            return HttpResponseRedirect(reverse('index'))

    else:
        club_form = ClubForm()

    return render(request, 'nomi/club_form.html', context={'form': club_form})


@login_required
def post_create(request, pk):
    parent = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        club = parent.club
        if post_form.is_valid():
            post = Post.objects.create(post_name=post_form.cleaned_data['post_title'], club=club, parent=parent)
            post_pk = post.pk

            return HttpResponseRedirect(reverse('nomi_create', kwargs={'pk': post_pk}))

    else:
        post_form = PostForm()

    if  request.user in parent.post_holders.all():
        return render(request, 'nomi/post_form.html', context={'form': post_form})
    else:
        return render(request,'no_access.html')


@login_required
def child_club_view(request, pk, view_pk):
    club = Club.objects.get(pk=pk)

    if club.status == 'Club created':
        approved = 1
    else:
        approved = 0

    view_pk = view_pk
    view = Club.objects.get(pk=view_pk)

    if view.perms == 'normal':
        power_to_approve = 0
    else:
        power_to_approve = 1

    view_parent = Club.objects.get(pk=view.club_parent.pk)

    if view_parent in club.club_approvals.all():
        approval = 1
    else:
        approval = 0

    return render(request, 'child_club.html', {'club': club, 'view_pk': view_pk, 'ap': approved,
                                               'approval': approval, 'power_to_approve': power_to_approve})


@login_required
def child_post_view(request, pk, view_pk):
    post = Post.objects.get(pk=pk)
    nominations = Nomination.objects.filter(nomi_post=post)

    if post.status == 'Post created':
        approved = 1
    else:
        approved = 0

    view_pk = view_pk
    view = Post.objects.get(pk=view_pk)

    if view.perms == 'normal':
        power_to_approve = 0
    else:
        power_to_approve = 1

    view_parent = Post.objects.get(pk=view.parent.pk)

    if view_parent in post.post_approvals.all():
        approval = 1
    else:
        approval = 0



    access = False
    for pt in post.post_approvals.all():
        if request.user in pt.post_holders.all():
            access=True
            break

    if access or request.user in post.parent.post_holders.all():
        return render(request, 'child_post.html', {'post': post, 'view_pk': view_pk, 'ap': approved,
                                               'approval': approval, 'power_to_approve': power_to_approve,
                                               'nominations': nominations})
    else:
        return render(request,'no_access.html')



@login_required
def club_approval(request, view_pk, club_pk):
    club = Club.objects.get(pk=club_pk)
    viewer = Club.objects.get(pk=view_pk)
    to_add = viewer.club_parent

    club.club_approvals.add(to_add)

    return HttpResponseRedirect(reverse('child_club', kwargs={'pk': club_pk, 'view_pk': view_pk}))


@login_required
def post_approval(request, view_pk, post_pk):
    post = Post.objects.get(pk=post_pk)
    viewer = Post.objects.get(pk=view_pk)
    to_add = viewer.parent

    post.post_approvals.add(to_add)

    access = False
    for apv_post in post.post_approvals.all():
        if request.user in apv_post.post_holders.all():
            access = True
            break

    if access or request.user in post.parent.post_holders.all():
        return HttpResponseRedirect(reverse('child_post', kwargs={'pk': post_pk, 'view_pk': view_pk}))
    else:
        return render(request,'no_access.html')


@login_required
def final_club_approval(request, view_pk, club_pk):
    club = Club.objects.get(pk=club_pk)
    viewer = Club.objects.get(pk=view_pk)
    to_add = viewer

    club.club_approvals.add(to_add)
    club.status = 'Club approved'
    club.save()

    return HttpResponseRedirect(reverse('child_club', kwargs={'pk': club_pk, 'view_pk': view_pk}))


@login_required
def final_post_approval(request, view_pk, post_pk):
    post = Post.objects.get(pk=post_pk)
    viewer = Post.objects.get(pk=view_pk)
    to_add = viewer
    post.post_approvals.add(to_add)
    post.status = 'Post approved'
    post.save()

    access = False
    for apv_post in post.post_approvals.all():
        if request.user in apv_post.post_holders.all():
            access = True
            break

    if access or request.user in post.parent.post_holders.all():
        return HttpResponseRedirect(reverse('child_post', kwargs={'pk': post_pk, 'view_pk': view_pk}))
    else:
        return render(request, 'no_access.html')


@login_required
def nomination_create(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        title_form = NominationForm(request.POST)
        if title_form.is_valid():
            post = Post.objects.get(pk=pk)

            questionnaire = Questionnaire.objects.create(name=title_form.cleaned_data['title'],
                                                         description=title_form.cleaned_data['description'])

            nomination = Nomination.objects.create(name=title_form.cleaned_data['title'],
                                                   description=title_form.cleaned_data['description'],
                                                   nomi_form=questionnaire, nomi_post=post,
                                                   year_choice=title_form.cleaned_data['year_choice'],
                                                   hall_choice=title_form.cleaned_data['hall_choice'],
                                                   dept_choice=title_form.cleaned_data['dept_choice'],
                                                   )

            pk = questionnaire.pk
            return HttpResponseRedirect(reverse('forms:creator_form', kwargs={'pk': pk}))

    else:
        title_form = NominationForm()

    return render(request, 'nomi/nomination_form.html', context={'form': title_form, 'post': post})


class NominationUpdate(UpdateView):
    model = Nomination
    fields = ['name', 'description', 'year_choice', 'hall_choice', 'dept_choice']
    success_url = reverse_lazy('index')


class NominationDelete(DeleteView):
    model = Nomination
    success_url = reverse_lazy('index')


def nomi_detail(request, view_pk, post_pk, nomi_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    questionnaire = nomi.nomi_form
    form = questionnaire.get_form(request.POST or None)

    if nomi.status == 'Nomination created':
        approved = 1
    else:
        approved = 0

    view = Post.objects.get(pk=view_pk)

    if view.perms == 'normal':
        power_to_send = 0
    else:
        power_to_send = 1

    view_parent = Post.objects.get(pk=view.parent.pk)

    if view_parent in nomi.nomi_approvals.all():
        approval = 1
    else:
        approval = 0

    access = False
    for apv_post in nomi.nomi_post.post_approvals.all():
        if request.user in apv_post.post_holders.all():
            access = True
            break

    if access or request.user in nomi.nomi_post.parent.post_holders.all():
        return render(request, 'nomi_detail.html', context={'nomi': nomi, 'form': form, 'view_pk': view_pk,
                                                        'post_pk': post_pk, 'ap': approved,
                                                        'approval': approval, 'power_to_send': power_to_send})
    else:
        return render(request, 'no_access.html')



@login_required
def nomi_approval(request, view_pk, post_pk, nomi_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    viewer = Post.objects.get(pk=view_pk)
    to_add = viewer.parent
    nomi.nomi_approvals.add(to_add)

    return HttpResponseRedirect(reverse('nomi_detail', kwargs={'post_pk': post_pk, 'view_pk': view_pk,
                                                               'nomi_pk': nomi_pk}))


@login_required
def final_nomi_approval(request, view_pk, post_pk,nomi_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    viewer = Post.objects.get(pk=view_pk)
    to_add = viewer
    nomi.nomi_approvals.add(to_add)
    nomi.open_to_users()
    nomi.save()

    return HttpResponseRedirect(reverse('nomi_detail', kwargs={'post_pk': post_pk, 'view_pk': view_pk,
                                                               'nomi_pk': nomi_pk}))


@login_required
def nomi_apply(request, pk):
    nomination = Nomination.objects.get(pk=pk)
    count = NominationInstance.objects.filter(nomination=nomination).filter(user=request.user).count()
    if not count:
        if nomination.nomi_form:
            questionnaire = nomination.nomi_form
            form = questionnaire.get_form(request.POST or None)
            form_confirm = ConfirmApplication(request.POST or None)

            if form_confirm.is_valid():
                if form.is_valid():
                    filled_form = questionnaire.add_answer(request.user, form.cleaned_data)
                    NominationInstance.objects.create(user=request.user, nomination=nomination, filled_form=filled_form)
                    info = "Your application has been recorded"
                    return render(request, 'nomi_done.html', context={'info': info})

            return render(request, 'forms/show_form.html', context={'form': form, 'form_confirm': form_confirm,
                                                                    'questionnaire': questionnaire, 'pk': pk})
        else:
            form_confirm = ConfirmApplication(request.POST or None)

            if form_confirm.is_valid():
                NominationInstance.objects.create(user=request.user, nomination=nomination)
                info = "Your application has been recorded"
                return render(request, 'nomi_done.html', context={'info': info})

    else:
        info = "You have applied for it already."
        return render(request, 'nomi_done.html', context={'info': info})


@login_required
def applications(request, pk):
    nomination = Nomination.objects.get(pk=pk)
    applicants = NominationInstance.objects.filter(nomination=nomination)

    return render(request, 'applicants.html', context={'applicants': applicants})


@login_required
def accept_nomination(request, pk):
    application = NominationInstance.objects.get(pk=pk)
    id_accept = application.nomination.pk
    application.status = 'Accepted'
    application.save()

    return HttpResponseRedirect(reverse('applicants', kwargs={'pk': id_accept}))


@login_required
def reject_nomination(request, pk):
    application = NominationInstance.objects.get(pk=pk)
    id_reject = application.nomination.pk
    application.status = 'Rejected'
    application.save()

    return HttpResponseRedirect(reverse('applicants', kwargs={'pk': id_reject}))


@login_required
def result(request, pk):
    nomination = Nomination.objects.get(pk=pk)
    users = NominationInstance.objects.filter(nomination=nomination).filter(status__exact='Accepted')
    return render(request, 'result.html', context={'users': users})


@login_required
def nomination_answer(request, pk):
    application = NominationInstance.objects.get(pk=pk)
    form1 = application.filled_form
    data = json.loads(form1.data)

    questionnaire = application.nomination.nomi_form
    form = questionnaire.get_form(data)

    return render(request, 'nomi_answer.html', context={'form': form, 'nomi': application})


@login_required
def profile_view(request):
    pk = request.user.pk

    try:
        user_profile = UserProfile.objects.get(user__id=pk)
        return render(request, 'profile.html', context={'user_profile': user_profile})
    except ObjectDoesNotExist:
        return HttpResponseRedirect('create')


class UserProfileCreate(CreateView):
    model = UserProfile
    fields = '__all__'
    success_url = reverse_lazy('index')


class UserProfileUpdate(UpdateView):
    model = UserProfile
    fields = '__all__'
    success_url = reverse_lazy('index')


@login_required
def universal_filter(request):
    filters = UserProfileFilter(request.GET, queryset=UserProfile.objects.all())
    return render(request, 'filters.html', {'filter': filters})



# not in use
@login_required
def nomi_edit(request, view_pk, post_pk,nomi_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    questionnaire = nomi.nomi_form
    form = questionnaire.get_form()
    ques_pk = questionnaire.pk
    questions = Question.objects.filter(questionnaire=questionnaire)

    return render(request, 'nomi_edit.html',
                  context={'form': form, 'questions': questions, 'nomi': nomi, view_pk: view_pk, post_pk: post_pk})
