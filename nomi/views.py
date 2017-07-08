import json
from itertools import chain
from operator import attrgetter
import pyperclip
import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from forms.models import Questionnaire
from gymkhana.settings import DOMAIN_NAME
from .forms import *
from .models import *



# main index view for user,contains all nomination to be filled by normal user,
# have club filter that filter both nomination and its group..
# is_safe

@login_required
def index(request):
    if request.user.is_authenticated:
        try:
            today = datetime.now()
            posts = Post.objects.filter(post_holders=request.user)
            username = UserProfile.objects.get(user=request.user)
            club_filter = ClubFilter(request.POST or None)
            if club_filter.is_valid():
                club = Club.objects.get(pk=club_filter.cleaned_data['club'])
                grouped_nomi = club.club_group.all().filter(status='out')
                nomi = club.club_nomi.all().filter(group_status='normal').filter(status='Nomination out')
                result_query = sorted(chain(nomi, grouped_nomi), key=attrgetter('opening_date'), reverse=True)


                return render(request, 'index1.html', context={'posts': posts, 'username': username,
                                                               'result_query': result_query, 'club_filter': club_filter,
                                                               'today': today})

            grouped_nomi = GroupNomination.objects.filter(status='out')
            nomi = Nomination.objects.filter(group_status='normal').filter(status='Nomination out')
            result_query = sorted(chain(nomi, grouped_nomi), key=attrgetter('opening_date'), reverse=True)


            return render(request, 'index1.html', context={'posts': posts, 'username': username,
                                                            'club_filter': club_filter,
                                                           'result_query': result_query,'today':today})

        except ObjectDoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
            pk = profile.pk
            return HttpResponseRedirect(reverse('profile_update', kwargs={'pk': pk}))

    else:
        return HttpResponseRedirect(reverse('login'))



# a view link for user who have some post....
# It include the all nomination that the given user have perms to see whether it is being created or out or in interview period...
# is_safe
# to add -------  nomi that the user has been added as panel ********

@login_required
def admin_portal(request):
    posts = Post.objects.filter(post_holders=request.user)
    username = UserProfile.objects.get(user=request.user)

    admin_query = Nomination.objects.none()

    for post in posts:
        query = Nomination.objects.filter(nomi_approvals=post)
        admin_query = admin_query | query

    admin_query = admin_query.distinct().exclude(status='Work done')
    admin_query_reverse = admin_query[::-1]

    club_filter = ClubFilter(request.POST or None)
    if club_filter.is_valid():
        club = Club.objects.get(pk=club_filter.cleaned_data['club'])
        admin_query = admin_query.filter(tags=club)
        admin_query_reverse = admin_query[::-1]

        return render(request, 'admin_portal.html', context={'posts': posts, 'username': username,
                                                             'admin_query': admin_query_reverse,
                                                             'club_filter': club_filter})

    return render(request, 'admin_portal.html', context={'posts': posts, 'username': username,
                                                         'admin_query': admin_query_reverse,
                                                         'club_filter': club_filter})



# a view for retification purpose
# is_safe

@login_required
def senate_view(request):
    nomi_ratify = Nomination.objects.filter(status='Sent for ratification')
    all_posts = Post.objects.filter(post_holders=request.user)
    access = False

    for post in all_posts:
        if post.perms == 'can ratify the post':
            access = True
            break

    if access:
        return render(request, 'senate_view.html', context={'nomi': nomi_ratify})

    else:
        return render(request, 'no_access.html')


## ----------------------------------------------------------------------------------------------------------------
##################    POST RELATED VIEWS   #####################
## ----------------------------------------------------------------------------------------------------------------

# a view for a given post....contains all thing required for working on that post...
# tips...use redirect if using form as button
# is_safe
@login_required
def post_view(request, pk):
    post = Post.objects.get(pk=pk)
    child_posts = Post.objects.filter(parent=post)
    child_posts_reverse = child_posts[::-1]

    post_approvals = Post.objects.filter(post_approvals=post).filter(status='Post created')
    nomi_approvals = Nomination.objects.filter(nomi_approvals=post).filter(status='Nomination created')
    group_nomi_approvals = GroupNomination.objects.filter(status='created').filter(approvals=post)


    result_approvals = Nomination.objects.filter(result_approvals=post).exclude(status='work_done').exclude(status='Nomination_created')

    if request.method == 'POST':
        tag_form = ClubForm(request.POST)
        if tag_form.is_valid():
            Club.objects.create(club_name=tag_form.cleaned_data['club_name'], club_parent=post.club)
            return HttpResponseRedirect(reverse('post_view', kwargs={'pk': pk}))
    else:
        tag_form = ClubForm


    if request.user in post.post_holders.all():
        return render(request, 'post1.html', context={'post': post, 'child_posts': child_posts_reverse,
                                                      'post_approval': post_approvals, 'tag_form': tag_form,
                                                      'nomi_approval': nomi_approvals,
                                                      'group_nomi_approvals': group_nomi_approvals,
                                                      'result_approvals': result_approvals})
    else:
        return render(request, 'no_access.html')


# view for parent post to create new child post
# is_safe

@login_required
def post_create(request, pk):
    parent = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post_form = PostForm(parent, request.POST)
        if post_form.is_valid():
            club_id = post_form.cleaned_data['club']
            club = Club.objects.get(pk=club_id)
            Post.objects.create(post_name=post_form.cleaned_data['post_name'],
                                       club=club, parent=parent)

            return HttpResponseRedirect(reverse('post_view', kwargs={'pk': pk}))

    else:
        club = parent.club
        post_form = PostForm(parent)

    if request.user in parent.post_holders.all():
        return render(request, 'nomi/post_form.html', context={'form': post_form, 'parent': parent})
    else:
        return render(request, 'no_access.html')


# view for child post related stuff for parent post only
# is_safe

@login_required
def child_post_view(request, pk):
    post = Post.objects.get(pk=pk)
    parent = post.parent
    nominations = Nomination.objects.filter(nomi_post=post)


    ## tag features
    tag_form = ClubForm(request.POST or None)
    if tag_form.is_valid():
        Club.objects.create(club_name=tag_form.cleaned_data['club_name'], club_parent=post.club)
        return HttpResponseRedirect(reverse('child_post', kwargs={'pk': pk}))


    give_form = BlankForm(request.POST or None)
    if give_form.is_valid():
        if post.tag_perms == 'normal':
            post.tag_perms = 'Can create'
        else:
            post.tag_perms = 'normal'

        post.save()
        return HttpResponseRedirect(reverse('child_post', kwargs={'pk': pk}))




    if request.user in parent.post_holders.all():
        return render(request, 'child_post1.html', {'post': post,'nominations': nominations,'parent':parent,
                                                    'tag_form': tag_form, 'give_form': give_form})

    else:
        return render(request, 'no_access.html')






@login_required
def post_approval(request, view_pk, post_pk):
    post = Post.objects.get(pk=post_pk)
    viewer = Post.objects.get(pk=view_pk)


    access = False
    for apv_post in post.post_approvals.all():
        if request.user in apv_post.post_holders.all():
            access = True
            break

    if access or request.user in post.parent.post_holders.all():
        to_add = viewer.parent
        post.post_approvals.add(to_add)
        post.tags.add(to_add.club)
        return HttpResponseRedirect(reverse('post_view', kwargs={'pk': view_pk}))
    else:
        return render(request, 'no_access.html')


@login_required
def post_reject(request, view_pk, post_pk):
    post = Post.objects.get(pk=post_pk)
    viewer = Post.objects.get(pk=view_pk)
    to_add = viewer

    access = False
    for apv_post in post.post_approvals.all():
        if request.user in apv_post.post_holders.all():
            access = True
            break

    if access:
        post.post_approvals.remove(to_add)

    return HttpResponseRedirect(reverse('post_view', kwargs={'pk': view_pk}))


@login_required
def final_post_approval(request, view_pk, post_pk):
    post = Post.objects.get(pk=post_pk)
    viewer = Post.objects.get(pk=view_pk)
    to_add = viewer.parent
    post.post_approvals.add(to_add)
    post.tags.add(to_add.club)
    post.status = 'Post approved'
    post.save()

    access = False
    for apv_post in post.post_approvals.all():
        if request.user in apv_post.post_holders.all():
            access = True
            break

    if access or request.user in post.parent.post_holders.all():
        return HttpResponseRedirect(reverse('post_view', kwargs={'pk': view_pk}))
    else:
        return render(request, 'no_access.html')


@login_required
def nomination_create(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        title_form = NominationForm(request.POST)
        if title_form.is_valid():
            post = Post.objects.get(pk=pk)

            questionnaire = Questionnaire.objects.create(name=title_form.cleaned_data['title'])

            nomination = Nomination.objects.create(name=title_form.cleaned_data['title'],
                                                   description=title_form.cleaned_data['description'],
                                                   deadline=title_form.cleaned_data['deadline'],
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
def nomi_detail(request, nomi_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    parents = nomi.nomi_post.parent.post_holders.all()
    questionnaire = nomi.nomi_form
    form = questionnaire.get_form(request.POST or None)

    panelform = UserId(request.POST or None)



    status = [None]*5

    if nomi.status == 'Nomination created':
        status[0] = True
    elif nomi.status == 'Nomination out':
        status[1] = True
    elif nomi.status == 'Interview period':
        status[2] = True
    elif nomi.status == 'Sent for ratification':
        status[3] = True
    else:
        status[4] = True

    access = False
    view_post = None
    for apv_post in nomi.nomi_approvals.all():
        if request.user in apv_post.post_holders.all():
            access = True
            view_post = apv_post
            break

    if access:
        if view_post.perms == 'normal':
            power_to_send = 0
        else:
            power_to_send = 1
        if view_post.parent in nomi.nomi_approvals.all():
            sent_to_parent = 1
        else:
            sent_to_parent = 0

        if panelform.is_valid():
            try:
                profile = UserProfile.objects.get(roll_no=panelform.cleaned_data["user_roll"])
                user = profile.user
                nomi.interview_panel.add(user)
                return HttpResponseRedirect(reverse('nomi_detail', kwargs={'nomi_pk': nomi_pk}))
            except ObjectDoesNotExist:
                return HttpResponseRedirect(reverse('nomi_detail', kwargs={'nomi_pk': nomi_pk}))

        panelists = nomi.interview_panel.all().distinct()
        panelists_exclude_parent = []

        for panelist in panelists:
            if panelist not in parents:
                panelists_exclude_parent.append(panelist)

        return render(request, 'nomi_detail_admin.html', context={'nomi': nomi, 'form': form, 'panelform': panelform,
                                                                  'sent_to_parent': sent_to_parent, 'status': status,
                                                                  'power_to_send': power_to_send, 'parents': parents,
                                                                  'panelists': panelists_exclude_parent})


    elif request.user in nomi.interview_panel.all():
        return render(request, 'nomi_detail_user.html', context={'nomi': nomi})


    else:
        if status[1]:
            return render(request, 'nomi_detail_user.html', context={'nomi': nomi})
        else:
            return render(request, 'no_access.html')


@login_required
def remove_panelist(request, nomi_pk, user_pk):
    nomination = Nomination.objects.get(pk=nomi_pk)
    panelist = User.objects.get(pk=user_pk)

    panel = nomination.interview_panel
    panel.remove(panelist)

    return HttpResponseRedirect(reverse('nomi_detail', kwargs={'nomi_pk': nomi_pk}))


@login_required
def nomi_approval(request, nomi_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    access = False
    view_post = 0
    for apv_post in nomi.nomi_approvals.all():
        if request.user in apv_post.post_holders.all():
            access = True
            view_post = apv_post
            break
    if access:
        to_add = view_post.parent
        nomi.nomi_approvals.add(to_add)
        nomi.tags.add(to_add.club)
        return HttpResponseRedirect(reverse('nomi_detail', kwargs={'nomi_pk': nomi_pk}))
    else:
        return render(request, 'no_access.html')


@login_required
def nomi_reject(request, nomi_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    access = False
    view_post = 0
    for apv_post in nomi.nomi_approvals.all():
        if request.user in apv_post.post_holders.all():
            access = True
            view_post = apv_post
            break
    if access:
        to_remove = view_post
        nomi.nomi_approvals.remove(to_remove)
        return HttpResponseRedirect(reverse('post_view', kwargs={'pk': view_post.pk}))
    else:
        return render(request, 'no_access.html')


@login_required
def final_nomi_approval(request, nomi_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    access = False
    view_post = 0
    for apv_post in nomi.nomi_approvals.all():
        if request.user in apv_post.post_holders.all():
            access = True
            view_post = apv_post
            break
    if access:
        to_add = view_post.parent
        nomi.tags.add(to_add.club)
        nomi.open_to_users()
        return HttpResponseRedirect(reverse('nomi_detail', kwargs={'nomi_pk': nomi_pk}))
    else:
        return render(request, 'no_access.html')


@login_required
def group_nominations(request, pk):
    post = Post.objects.get(pk=pk)
    child_posts = Post.objects.filter(parent=post)
    child_posts_reverse = child_posts[::-1]
    post_approvals = Post.objects.filter(post_approvals=post).filter(status='Post created')
    nomi_approvals = Nomination.objects.filter(nomi_approvals=post).filter(status='Nomination created')

    if request.method == 'POST':
        groupform = SelectNomiForm(post, request.POST)
        title_form = GroupNominationForm(request.POST)
        if title_form.is_valid():
            if groupform.is_valid():
                group = GroupNomination.objects.create(name=title_form.cleaned_data['title'],
                                                       description=title_form.cleaned_data['description'])
                group.approvals.add(post)
                for nomi_pk in groupform.cleaned_data['group']:
                    # things to be performed on nomination
                    nomi = Nomination.objects.get(pk=nomi_pk)
                    group.nominations.add(nomi)
                    for tag in nomi.tags.all():
                        group.tags.add(tag)
                    nomi.group_status = 'grouped'
                    to_add = post.parent
                    nomi.nomi_approvals.add(to_add)
                    nomi.save()
                    nomi.open_to_users()
                return HttpResponseRedirect(reverse('post_view', kwargs={'pk': pk}))

    else:
        title_form = GroupNominationForm
        groupform = SelectNomiForm(post)

    return render(request, 'nomi_group.html', context={'post': post, 'child_posts': child_posts_reverse,
                                                       'post_approval': post_approvals, 'nomi_approval': nomi_approvals,
                                                       'form': groupform, 'title_form': title_form})


@login_required
def group_nomi_detail(request, pk):
    group_nomi = GroupNomination.objects.get(pk = pk)
    admin = 0
    for post in request.user.posts.all():
        if post in group_nomi.approvals.all():
            admin = post

    form_confirm = ConfirmApplication(request.POST or None)
    if form_confirm.is_valid():
        group_nomi.status = 'out'
        group_nomi.save()

    return render(request, 'group_detail.html', {'group_nomi': group_nomi, 'admin': admin,
                                                 'form_confirm': form_confirm})


@login_required
def add_to_group(request, pk, gr_pk):
    post = Post.objects.get(pk=pk)
    child_posts = Post.objects.filter(parent=post)
    child_posts_reverse = child_posts[::-1]
    post_approvals = Post.objects.filter(post_approvals=post).filter(status='Post created')
    nomi_approvals = Nomination.objects.filter(nomi_approvals=post).filter(status='Nomination created')

    if request.method == 'POST':
        groupform = SelectNomiForm(post, request.POST)
        if groupform.is_valid():
            group = GroupNomination.objects.get(pk=gr_pk)

            for nomi_pk in groupform.cleaned_data['group']:
                # things to be performed on nomination
                nomi = Nomination.objects.get(pk=nomi_pk)
                group.nominations.add(nomi)
                for tag in nomi.tags.all():
                    group.tags.add(tag)
                nomi.group_status = 'grouped'
                to_add = post.parent
                nomi.nomi_approvals.add(to_add)
                nomi.save()
                nomi.open_to_users()
            return HttpResponseRedirect(reverse('group_nomi_detail', kwargs={'pk': gr_pk}))

    else:
        title_form = None
        groupform = SelectNomiForm(post)

    return render(request, 'nomi_group.html', context={'post': post, 'child_posts': child_posts_reverse,
                                                       'post_approval': post_approvals, 'nomi_approval': nomi_approvals,
                                                       'form': groupform, 'title_form': title_form})


@login_required
def remove_from_group(request, nomi_pk, gr_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    group = GroupNomination.objects.get(pk=gr_pk)
    group.nominations.remove(nomi)

    nomi.group_status = 'normal'
    nomi.status = 'Nomination created'
    nomi.save()

    return HttpResponseRedirect(reverse('group_nomi_detail', kwargs={'pk': gr_pk}))


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
def copy_nomi_link(request, pk):
    url = DOMAIN_NAME + '/nominations/nomi_detail/' + str(pk) + '/'
    pyperclip.copy(url)

    return HttpResponseRedirect(reverse('admin_portal'))



@login_required
def applications(request, pk):
    nomination = Nomination.objects.get(pk=pk)
    applicants = NominationInstance.objects.filter(nomination=nomination)
    accepted = NominationInstance.objects.filter(nomination=nomination).filter(status='Accepted')
    rejected = NominationInstance.objects.filter(nomination=nomination).filter(status='Rejected')
    pending = NominationInstance.objects.filter(nomination=nomination).filter(status=None)

    status = [None]*5

    if nomination.status == 'Nomination created':
        status[0] = True
    elif nomination.status == 'Nomination out':
        status[1] = True
    elif nomination.status == 'Interview period':
        status[2] = True
    elif nomination.status == 'Sent for ratification':
        status[3] = True
    else:
        status[4] = True

    view_post = None
    access = False
    for apv_post in nomination.nomi_approvals.all():
        if request.user in apv_post.post_holders.all():
            view_post = apv_post
            access = True
            break

# if user post in parent tree
    if access:
        permission = None
        senate_permission = None

        if view_post.perms == 'can approve post and send nominations to users':
            permission = True
            senate_permission = False
        elif view_post.perms == 'can ratify the post':
            senate_permission = True
            permission = False

        # result approval things    send,sent,cancel
        results_approval = [None]*3

        if view_post in nomination.result_approvals.all():
            if view_post.parent in nomination.result_approvals.all():
                results_approval[1] = True
                grand_parent = view_post.parent.parent
                if grand_parent not in nomination.result_approvals.all():
                    results_approval[2] = True
            else:
                results_approval[0] = True

        form_confirm = ConfirmApplication(request.POST or None)

        if form_confirm.is_valid():
            nomination.status = 'Interview period'
            nomination.save()
            return HttpResponseRedirect(reverse('applicants', kwargs={'pk': pk}))
        return render(request, 'applicants.html', context={'nomination': nomination, 'applicants': applicants,
                                                           'form_confirm': form_confirm,
                                                           'result_approval': results_approval,
                                                           'accepted': accepted, 'rejected': rejected, 'status': status,
                                                           'pending': pending, 'perm': permission,
                                                           'senate_perm': senate_permission})



    ## if user in panel...
    if request.user in nomination.interview_panel.all():
        return render(request, 'applicant_panel.html', context={'nomination': nomination, 'applicants': applicants,
                                                                'accepted': accepted, 'rejected': rejected,
                                                                'pending': pending,  'status': status})

    if not access:
        return render(request, 'no_access.html')




@login_required
def nomination_answer(request, pk):
    application = NominationInstance.objects.get(pk=pk)
    ans_form = application.filled_form
    data = json.loads(ans_form.data)
    applicant = application.user.userprofile
    questionnaire = application.nomination.nomi_form
    form = questionnaire.get_form(data)


    comments = Commment.objects.filter(nomi_instance=application)
    comments_reverse = comments[::-1]
    comment_form = CommentForm(request.POST or None)

    all_posts = Post.objects.filter(post_holders=request.user)
    nomination = application.nomination
    auth_user = UserProfile.objects.get(user=request.user)

    senate_perm = False
    for post in all_posts:
        if post.perms == 'can ratify the post':
            senate_perm = True
            break

    inst_user = False
    if application.user == request.user:
        inst_user = True



    view_post = None
    for post in nomination.nomi_approvals.all():
        if post in all_posts:
            view_post = post
            break

    # result approval things    send,sent,cancel
    results_approval = [None]*3

    if view_post in nomination.result_approvals.all():
        if view_post.parent in nomination.result_approvals.all():
            results_approval[1] = True
            grand_parent = view_post.parent.parent
            if grand_parent not in nomination.result_approvals.all():
                results_approval[2] = True
        else:
            results_approval[0] = True

    if request.user in nomination.interview_panel.all():
        view_post = nomination.nomi_post.parent
        if view_post.parent in nomination.result_approvals.all():
            results_approval[1] = True
            grand_parent = view_post.parent.parent
            if grand_parent not in nomination.result_approvals.all():
                results_approval[2] = True
        else:
            results_approval[0] = True


    if comment_form.is_valid():
        Commment.objects.create(comments=comment_form.cleaned_data['comment'],
                                nomi_instance=application, user=request.user)
        return HttpResponseRedirect(reverse('nomi_answer', kwargs={'pk': pk}))

    return render(request, 'nomi_answer.html', context={'form': form, 'nomi': application, 'nomi_user': applicant,
                                                        'comment_form': comment_form, 'inst_user': inst_user,
                                                        'comments': comments_reverse, 'senate_perm': senate_perm,
                                                        'nomi_pk': nomination.pk, 'result_approval': results_approval,
                                                        'auth_user': auth_user})



@login_required
def ratify(request, nomi_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    access = False
    view_post = None

    for apv_post in nomi.nomi_approvals.all():
        if request.user in apv_post.post_holders.all():
            access = True
            view_post = apv_post
            break
    if access:
        to_add = view_post.parent
        nomi.result_approvals.add(to_add)
        nomi.nomi_approvals.add(to_add)
        nomi.status = 'Sent for ratification'
        nomi.save()

        return HttpResponseRedirect(reverse('applicants', kwargs={'pk': nomi_pk}))

    else:
        return render(request, 'no_access.html')


@login_required
def cancel_ratify(request, nomi_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    access = False
    view_post = None

    for apv_post in nomi.nomi_approvals.all():
        if request.user in apv_post.post_holders.all():
            access = True
            view_post = apv_post
            break
    if access:
        to_remove = view_post.parent
        nomi.result_approvals.remove(to_remove)
        nomi.nomi_approvals.remove(to_remove)
        nomi.status = 'Interview period'
        nomi.save()

        return HttpResponseRedirect(reverse('applicants', kwargs={'pk': nomi_pk}))

    else:
        return render(request, 'no_access.html')


@login_required
def cancel_result_approval(request, nomi_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    access = False
    view_post = None
    for apv_post in nomi.nomi_approvals.all():
        if request.user in apv_post.post_holders.all():
            access = True
            view_post = apv_post
            break
    if access:
        to_remove = view_post.parent
        if to_remove.parent not in nomi.result_approvals.all():
            nomi.result_approvals.remove(to_remove)
        return HttpResponseRedirect(reverse('applicants', kwargs={'pk': nomi_pk}))
    else:
        return render(request, 'no_access.html')


@login_required
def result_approval(request, nomi_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    access = False
    view_post = None
    for apv_post in nomi.nomi_approvals.all():
        if request.user in apv_post.post_holders.all():
            access = True
            view_post = apv_post
            break
    if access:
        to_add = view_post.parent
        nomi.result_approvals.add(to_add)
        return HttpResponseRedirect(reverse('applicants', kwargs={'pk': nomi_pk}))
    else:
        return render(request, 'no_access.html')


@login_required
def accept_nomination(request, pk):
    application = NominationInstance.objects.get(pk=pk)
    id_accept = application.nomination.pk
    application.status = 'Accepted'
    application.save()

    return HttpResponseRedirect(reverse('applicants', kwargs={'pk': id_accept}))


@login_required
def mark_as_interviewed(request, pk):
    application = NominationInstance.objects.get(pk=pk)
    id_nomi = application.nomination.pk
    application.interview_status = 'Interview Done'
    application.save()

    return HttpResponseRedirect(reverse('applicants', kwargs={'pk': id_nomi}))


@login_required
def reject_nomination(request, pk):
    application = NominationInstance.objects.get(pk=pk)
    id_reject = application.nomination.pk
    application.status = 'Rejected'
    application.save()

    return HttpResponseRedirect(reverse('applicants', kwargs={'pk': id_reject}))


@login_required
def append_user(request, pk):
    nomi = Nomination.objects.get(pk=pk)
    nomi.append()
    return HttpResponseRedirect(reverse('applicants', kwargs={'pk': pk}))


@login_required
def replace_user(request, pk):
    nomi = Nomination.objects.get(pk=pk)
    nomi.replace()
    return HttpResponseRedirect(reverse('applicants', kwargs={'pk': pk}))



@login_required
def profile_view(request):
    pk = request.user.pk
    history = PostHistory.objects.filter(user=request.user)
    pending_nomi = NominationInstance.objects.filter(user=request.user).filter(nomination__status='Nomination out')
    interview_nomi = NominationInstance.objects.filter(user=request.user).filter(nomination__status='Interview period')
    declared_nomi = NominationInstance.objects.filter(user=request.user).\
        filter(nomination__status='Sent for ratification')

    try:
        user_profile = UserProfile.objects.get(user__id=pk)
        return render(request, 'profile.html', context={'user_profile': user_profile, 'history': history,
                                                        'pending_nomi': pending_nomi, 'declared_nomi': declared_nomi,
                                                        'interview_nomi': interview_nomi})
    except ObjectDoesNotExist:
        return HttpResponseRedirect('create')


@login_required
def public_profile(request, pk):
    student = UserProfile.objects.get(pk=pk)
    student_user = student.user
    history = PostHistory.objects.filter(user=student_user)
    my_posts = Post.objects.filter(post_holders=student_user)

    return render(request, 'public_profile.html', context={'student': student, 'history': history,
                                                           'my_posts': my_posts})


class UserProfileCreate(CreateView):
    model = UserProfile
    fields = ['name', 'roll_no', 'year', 'programme', 'department', 'user_img', 'hall', 'room_no', 'contact']
    success_url = reverse_lazy('index')


class UserProfileUpdate(UpdateView):
    model = UserProfile
    fields = ['name', 'roll_no', 'year', 'programme', 'department', 'user_img', 'hall', 'room_no', 'contact']
    success_url = reverse_lazy('index')


class CommentUpdate(UpdateView):
    model = Commment
    fields = ['comments']
    def get_success_url(self):
        form_pk = self.kwargs['form_pk']
        return reverse('nomi_answer', kwargs={'pk': form_pk})




class CommentDelete(DeleteView):
    model = Commment
    def get_success_url(self):
        form_pk = self.kwargs['form_pk']
        return reverse('nomi_answer', kwargs={'pk': form_pk})





