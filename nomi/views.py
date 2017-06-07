from django.shortcuts import render
from .models import Nomination, NominationInstance, UserProfile, Post, Club
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from .forms import NominationForm, PostForm, ConfirmApplication, NomiEdit
from forms.models import Questionnaire
from .filters import UserProfileFilter
import json

# the main view
@login_required
def index(request):
    nominations = Nomination.objects.all()
    all_nominations = nominations[::-1]
    posts = Post.objects.filter(post_holders=request.user)
    clubs = Club.objects.filter(club_members=request.user)
    username = UserProfile.objects.get(user=request.user)

    return render(request, 'index.html', context={'all_nominations': all_nominations, 'posts': posts,
                                                  'clubs': clubs, 'username': username})


# each club detail of user
@login_required
def club_view(request, pk):
    club = Club.objects.get(pk=pk)
    child_clubs = Club.objects.filter(club_parent=club)
    posts = Post.objects.filter(post_holders=request.user)

    return render(request, 'club.html', context={'club': club, 'child_clubs': child_clubs, 'posts': posts})


# each post detail of user from index
@login_required
def post_view(request, pk):
    post = Post.objects.get(pk=pk)
    child_posts = Post.objects.filter(parent=post)
    child_posts_reverse = child_posts[::-1]
    post_approval = Post.objects.filter(post_approvals=post).filter(status='Post created')

    return render(request, 'post.html', context={'post': post, 'child_posts': child_posts_reverse,
                                                 'post_approval': post_approval})
# new child post creation
@login_required
def post_create(request, pk):
    if request.method == 'POST':
        parent = Post.objects.get(pk=pk)
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            post = Post.objects.create(post_name=post_form.cleaned_data['post_title'], parent=parent)
            post_pk = post.pk

            return HttpResponseRedirect(reverse('nomi_create', kwargs={'pk': post_pk}))

    else:
        post_form = PostForm()

    return render(request, 'nomi/post_form.html', context={'form': post_form})


#detail view of child post
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

    return render(request, 'child_post.html', {'post': post, 'view_pk': view_pk, 'ap': approved,
                                               'approval': approval, 'power_to_approve': power_to_approve,
                                               'nominations': nominations})

# acts like a link  for approvalof posts
@login_required
def post_approval(request, view_pk, post_pk):
    post = Post.objects.get(pk=post_pk)
    viewer = Post.objects.get(pk=view_pk)
    to_add = viewer.parent
    post.post_approvals.add(to_add)

    return HttpResponseRedirect(reverse('child_post', kwargs={'pk': post_pk, 'view_pk': view_pk}))


@login_required
def final_post_approval(request, view_pk, post_pk):
    post = Post.objects.get(pk=post_pk)
    viewer = Post.objects.get(pk=view_pk)
    to_add = viewer
    post.post_approvals.add(to_add)
    post.status = 'Post approved'
    post.save()

    return HttpResponseRedirect(reverse('child_post', kwargs={'pk': post_pk, 'view_pk': view_pk}))



# view to create nomination
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

# detail view of a nomination
def nomi_detail(request,view_pk,post_pk,nomi_pk):
    nomi=Nomination.objects.get(pk=nomi_pk)
    questionnaire = nomi.nomi_form
    form = questionnaire.get_form(request.POST or None)

    if nomi.status == 'Nomination created':
        ap=1
    else:
        ap=0

    view = Post.objects.get(pk=view_pk)

    if view.perms == 'normal':
        power_to_send = 0
    else:
        power_to_send = 0


    view_parent = Post.objects.get(pk=view.parent.pk)

    if view_parent in nomi.nomi_approvals.all():
        approval = 1
    else:
        approval = 0


    return render(request, 'nomi_detail.html',context={'nomi':nomi, 'form': form,'view_pk':view_pk,'post_pk':post_pk,'ap': ap,
                                               'approval': approval, 'power_to_send': power_to_send,})


# nomi approvals

@login_required
def nomi_approval(request, view_pk,post_pk,nomi_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    viewer = Post.objects.get(pk=view_pk)
    to_add = viewer.parent
    nomi.nomi_approvals.add(to_add)

    return HttpResponseRedirect(reverse('nomi_detail', kwargs={'post_pk': post_pk, 'view_pk': view_pk,'nomi_pk':nomi_pk}))


@login_required
def final_nomi_approval(request, view_pk, post_pk,nomi_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    viewer = Post.objects.get(pk=view_pk)
    to_add = viewer
    nomi.nomi_approvals.add(to_add)
    nomi.status = 'Nomination out'
    nomi.save()

    return HttpResponseRedirect(reverse('nomi_detail', kwargs={'post_pk': post_pk, 'view_pk': view_pk,'nomi_pk':nomi_pk}))


# view for user to apply

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



<<<<<<< HEAD
# list of filled forms
def applications(request, pk):
=======
@login_required
def application_result(request, pk):
>>>>>>> a8feea9d87144abf478276d28b4aae7bf9c8595a
    nomination = Nomination.objects.get(pk=pk)
    applicants = NominationInstance.objects.filter(nomination=nomination)

    return render(request, 'applicants.html', context={'applicants': applicants})

# has to work on this
@login_required
def accept_nomination(request, pk):
    application = NominationInstance.objects.get(pk=pk)
    id_accept = application.nomination.pk
    application.status = 'a'
    application.save()

    return HttpResponseRedirect(reverse('applicants', kwargs={'pk': id_accept}))


@login_required
def reject_nomination(request, pk):
    application = NominationInstance.objects.get(pk=pk)
    id_reject = application.nomination.pk
    application.status = 'r'
    application.save()

    return HttpResponseRedirect(reverse('applicants', kwargs={'pk': id_reject}))

def result(request, pk):
    nomination = Nomination.objects.get(pk=pk)
    users = NominationInstance.objects.filter(nomination=nomination).filter(status__exact='a')

    return render(request, 'result.html', context={'users': users})




# viw to show filled forms by user
@login_required
def nomination_answer(request, pk):
    application = NominationInstance.objects.get(pk=pk)
    form1 = application.filled_form
    data = json.loads(form1.data)

    questionnaire = application.nomination.nomi_form
    form = questionnaire.get_form(data)

    return render(request, 'nomi_answer.html', context={'form': form, 'nomi': application})





# user data views
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


<<<<<<< HEAD
=======
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


@login_required
def post_create(request, pk):
    if request.method == 'POST':
        parent = Post.objects.get(pk=pk)
        post_form = PostForm(request.POST)
        club = parent.club

        if post_form.is_valid():
            post = Post.objects.create(post_name=post_form.cleaned_data['post_title'],
                                       club=club, parent=parent)
            post_pk = post.pk

            return HttpResponseRedirect(reverse('nomi_create', kwargs={'pk': post_pk}))

    else:
        post_form = PostForm()

    return render(request, 'nomi/post_form.html', context={'form': post_form})
>>>>>>> a8feea9d87144abf478276d28b4aae7bf9c8595a


@login_required
def universal_filter(request):
    filter = UserProfileFilter(request.GET, queryset=UserProfile.objects.all())
    return render(request, 'filters.html', {'filter': filter})




### no use as of now
def nomi_edit(request, view_pk, post_pk,nomi_pk):
    nomi=Nomination.objects.get(pk=nomi_pk)
    questionnaire = nomi.nomi_form
<<<<<<< HEAD
    form = questionnaire.get_form()
    pk = questionnaire.pk
    questions = Question.objects.filter(questionnaire=questionnaire)

    return render(request, 'nomi_edit.html',
                  context={'form': form, 'questions': questions, 'nomi':nomi , view_pk:view_pk , post_pk:post_pk})
=======
    form = questionnaire.get_form(request.POST or None)

    if nomi.status == 'Nomination created':
        ap=1
    else:
        ap=0

    view = Post.objects.get(pk=view_pk)

    if view.perms == 'normal':
        power_to_send = 0
    else:
        power_to_send = 0

    view_parent = Post.objects.get(pk=view.parent.pk)

    if view_parent in nomi.nomi_approvals.all():
        approval = 1
    else:
        approval = 0

    return render(request, 'nomi_detail.html',context={'nomi':nomi, 'form': form,'view_pk':view_pk,'post_pk':post_pk,'ap': ap,
                                               'approval': approval, 'power_to_send': power_to_send,})
>>>>>>> a8feea9d87144abf478276d28b4aae7bf9c8595a
