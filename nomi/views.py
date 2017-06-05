from django.shortcuts import render
from .models import Nomination, NominationInstance, UserProfile, Post, Club
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from .forms import NominationForm, PostForm
from forms.models import Questionnaire
from .filters import UserProfileFilter


@login_required
def index(request):
    nominations = Nomination.objects.all()
    all_nominations = nominations[::-1]
    posts = Post.objects.filter(post_holders=request.user)
    clubs = Club.objects.filter(club_members=request.user)

    return render(request, 'index.html', context={'all_nominations': all_nominations, 'posts': posts, 'clubs': clubs})


@login_required
def post_view(request, pk):
    post = Post.objects.get(pk=pk)
    child_posts = Post.objects.filter(parent=post)
    child_posts_reverse = child_posts[::-1]
    post_approval = Post.objects.filter(post_approvals=post)

    return render(request, 'post.html', context={'post': post, 'child_posts': child_posts_reverse,
                                                 'post_approval': post_approval})

@login_required
def club_view(request, pk):
    club = Club.objects.get(pk=pk)
    child_clubs = Club.objects.filter(club_parent=club)
    posts = Post.objects.filter(post_holders=request.user)

    return render(request, 'club.html', context={'club': club, 'child_clubs': child_clubs, 'posts': posts})


@login_required
def nomi_apply(request, pk):
    nomination = Nomination.objects.get(pk=pk)
    ct = NominationInstance.objects.filter(nomination=nomination).filter(user=request.user).count()

    if not request.user.is_superuser:
        if not ct:
             ins = NominationInstance.objects.create(user=request.user, nomination=nomination)
             info = "Your application has been recorded"
             return render(request, 'nomi_done.html', context={'info': info})
        else:
            info = "You have applied for it already."

    else:
        info = "The nomination for your post has been created and is awaiting responses"
        return render(request, 'nomi_done.html', context={'info': info})

    return render(request, 'nomi_done.html', context={'info': info})


def result(request, pk):
    nomination = Nomination.objects.get(pk=pk)
    users = NominationInstance.objects.filter(nomination=nomination).filter(status__exact='a')

    return render(request, 'result.html', context={'users': users})


@permission_required('nomi.admin')
def application_result(request, pk):
    nomination = Nomination.objects.filter(pk=pk)
    applicants = NominationInstance.objects.filter(nomination=nomination)

    return render(request, 'applicants.html', context={'applicants': applicants})


@login_required
@permission_required('nomi.admin')
def accept_nomination(request, pk):
    application = NominationInstance.objects.get(pk=pk)
    id_accept = application.nomination.pk
    application.status = 'a'
    application.save()

    return HttpResponseRedirect(reverse('applicants', kwargs={'pk': id_accept}))


@login_required
@permission_required('nomi.admin')
def reject_nomination(request, pk):
    application = NominationInstance.objects.get(pk=pk)
    id_reject = application.nomination.pk
    application.status = 'r'
    application.save()

    return HttpResponseRedirect(reverse('applicants', kwargs={'pk': id_reject}))


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
def nomination_create(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        title_form = NominationForm(request.POST)
        if title_form.is_valid():
            post=Post.objects.get(pk=pk)

            questionnaire = Questionnaire.objects.create(name=title_form.cleaned_data['title'],
                                                         description=title_form.cleaned_data['description'])
            nomination = Nomination.objects.create(name=title_form.cleaned_data['title'],
                                                 description=title_form.cleaned_data['description'],
                                                 nomi_form=questionnaire,nomi_post=post)
            pk = questionnaire.pk
            return HttpResponseRedirect(reverse('forms:creator_form', kwargs={'pk': pk}))

    else:
        title_form = NominationForm()
        post = Post.objects.get(pk=pk)

    return render(request, 'nomi/nomination_form.html', context={'form': title_form, 'post': post})


class NominationUpdate(UpdateView):
    model = Nomination
    fields = ['name', 'description']
    success_url = reverse_lazy('index')


class NominationDelete(DeleteView):
    model = Nomination
    success_url = reverse_lazy('index')


@login_required
def post_create(request, pk):     # TODO
    if request.method == 'POST':
        parent = Post.objects.get(pk=pk)
        post_form = PostForm(request.POST)
        club_name = parent.club
        if post_form.is_valid():
            post = Post.objects.create(post_name=post_form.cleaned_data['post_title'], parent=parent,club=club,)
            return HttpResponseRedirect(reverse('nomi_create', kwargs={'pk': pk}))

    else:
        post_form = PostForm()

    return render(request, 'nomi/post_form.html', context={'form': post_form})


@login_required
def universal_filter(request):
    filter = UserProfileFilter(request.GET, queryset=UserProfile.objects.all())
    return render(request, 'filters.html', {'filter': filter})

def post_approval(request,view_pk,post_pk):
    post=Post.objects.get(pk=post_pk)
    viewer=Post.objects.get(pk=view_pk)
    to_add=viewer.parent
    post.post_approvals.add(to_add)
    return HttpResponseRedirect(reverse('child_post' , kwargs={'pk':post_pk,'view_pk':view_pk}))


def child_post_view(request,pk,view_pk):
    post=Post.objects.get(pk=pk)
    if post.status == 'Post created':
        ap=1
    else:
        ap=0
    view_pk=view_pk
    view=Post.objects.get(pk=view_pk)
    view_parent=Post.objects.get(pk=view.parent.pk)
    if view_parent in post.post_approvals.all():
        approval=1
    else:
        approval=0
    return render(request,'child_post.html',{'post':post,'view_pk':view_pk,'ap':ap,'approval':approval})
