import json
from itertools import chain
from operator import attrgetter
import pyperclip

from datetime import date,datetime
import csv

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render,HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from forms.models import Questionnaire
from forms.views import replicate
from gymkhana.settings import DOMAIN_NAME
from .forms import *
from .models import *
from .scraper import getRecord


## ------------------------------------------------------------------------------------------------------------------ ##
############################################     DASHBOARD VIEWS     ###################################################
## ------------------------------------------------------------------------------------------------------------------ ##


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
                if club_filter.cleaned_data['club'] == 'NA':
                    club_filter = ClubFilter
                    grouped_nomi = GroupNomination.objects.filter(status='out')
                    nomi = Nomination.objects.filter(group_status='normal').filter(status='Nomination out')
                    re_nomi = Nomination.objects.filter(group_status='normal'). \
                        filter(status='Interview period and Nomination reopened')
                    nomi = nomi | re_nomi

                    result_query = sorted(chain(nomi, grouped_nomi), key=attrgetter('opening_date'), reverse=True)

                    return render(request, 'index1.html', context={'posts': posts, 'username': username,
                                                                   'club_filter': club_filter, 'today': today,
                                                                   'result_query': result_query})



                club = Club.objects.get(pk=club_filter.cleaned_data['club'])
                grouped_nomi = club.club_group.all().filter(status='out')
                nomi = club.club_nomi.all().filter(group_status='normal').filter(status='Nomination out')
                re_nomi = club.club_nomi.all().filter(group_status='normal').\
                    filter(status='Interview period and Nomination reopened')
                nomi = nomi | re_nomi
                result_query = sorted(chain(nomi, grouped_nomi), key=attrgetter('opening_date'), reverse=True)


                return render(request, 'index1.html', context={'posts': posts, 'username': username,
                                                               'result_query': result_query, 'club_filter': club_filter,
                                                               'today': today})

            grouped_nomi = GroupNomination.objects.filter(status='out')
            nomi = Nomination.objects.filter(group_status='normal').filter(status='Nomination out')
            re_nomi = Nomination.objects.filter(group_status='normal').\
                filter(status='Interview period and Nomination reopened')
            nomi = nomi | re_nomi

            result_query = sorted(chain(nomi, grouped_nomi), key=attrgetter('opening_date'), reverse=True)


            return render(request, 'index1.html', context={'posts': posts, 'username': username,
                                                           'club_filter': club_filter, 'today': today,
                                                           'result_query': result_query})

        except ObjectDoesNotExist:
            form = UserId(request.POST or None)
            if form.is_valid():
                data = getRecord(form.cleaned_data['user_roll'])
                email = str(request.user) + '@iitk.ac.in'
                if email == data['email']:
                    profile = UserProfile.objects.create(user=request.user,name = data['name'],roll_no = data['roll'],
                                                     programme = data["program"],department = data['department'],
                                                     contact = data['mobile'], room_no = data['room'])

                    pk = profile.pk
                    return HttpResponseRedirect(reverse('profile_update', kwargs={'pk': pk}))

                else:
                    info = "Please give correct roll no"
                    return render(request, 'nomi_done.html', context={'info': info})

            return render(request, 'register.html', context={'form': form})




    else:
        return HttpResponseRedirect(reverse('login'))


# contain all nomination for which user have rights whether created by him or created by his chil post
# also shows nomination for which he has been added as interview panel
# is_safe
@login_required
def admin_portal(request):
    posts = Post.objects.filter(post_holders=request.user)
    username = UserProfile.objects.get(user=request.user)

    admin_query = Nomination.objects.none()

    for post in posts:
        query = Nomination.objects.filter(nomi_approvals=post)
        admin_query = admin_query | query

    panel_nomi = request.user.panel.all().exclude(status='Nomination created')

    admin_query = admin_query | panel_nomi

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


@login_required
def interview_list(request):
    interviews = Nomination.objects.filter(interview_panel=request.user).exclude(status = 'Work done')

    return render(request, 'interviews.html', context={'interviews': interviews})


## ------------------------------------------------------------------------------------------------------------------ ##
#########################################    POST RELATED VIEWS   ######################################################
## ------------------------------------------------------------------------------------------------------------------ ##

'''
a view for a given post....contains all things required for working on that post...
tips...use redirect if using form as button
is_safe
'''
@login_required
def post_view(request, pk):
    post = Post.objects.get(pk=pk)
    child_posts = Post.objects.filter(parent=post)
    child_posts_reverse = child_posts[::-1]

    post_approvals = Post.objects.filter(post_approvals=post).filter(status='Post created')
    post_to_be_approved = Post.objects.filter(take_approval = post).filter(status = 'Post created')
    post_count = post_to_be_approved.count()
    post_approvals = post_to_be_approved|post_approvals
    post_approvals = post_approvals.distinct()

    entity_approvals = ClubCreate.objects.filter(take_approval=post)
    entity_by_me = ClubCreate.objects.filter(requested_by=post)

    nomi_approvals = Nomination.objects.filter(nomi_approvals=post).filter(status='Nomination created')
    re_nomi_approval = ReopenNomination.objects.filter(approvals=post).\
        filter(nomi__status='Interview period and Reopening initiated')
    group_nomi_approvals = GroupNomination.objects.filter(status='created').filter(approvals=post)
    count = nomi_approvals.count() + group_nomi_approvals.count() + re_nomi_approval.count()

    result_approvals = Nomination.objects.filter(result_approvals=post).exclude(status='Work done').\
        exclude(status='Nomination created').exclude(status='Nomination out')
    to_deratify = Deratification.objects.filter(deratify_approval = post).filter(status = 'requested')

    if request.method == 'POST':
        tag_form = ClubForm(request.POST)
        if tag_form.is_valid():
            if post.perms == "can ratify the post":
                Club.objects.create(club_name=tag_form.cleaned_data['club_name'], club_parent=post.club)
            else:
                ClubCreate.objects.create(club_name=tag_form.cleaned_data['club_name'], club_parent=post.club,
                                          take_approval=post.parent, requested_by=post)
            return HttpResponseRedirect(reverse('post_view', kwargs={'pk': pk}))

    else:
        tag_form = ClubForm



    if request.user in post.post_holders.all():
        return render(request, 'post1.html', context={'post': post, 'child_posts': child_posts_reverse,
                                                      'post_approval': post_approvals, 'tag_form': tag_form,
                                                      'nomi_approval': nomi_approvals,
                                                      'group_nomi_approvals': group_nomi_approvals,
                                                      'entity_by_me': entity_by_me, 're_nomi_approval': re_nomi_approval,
                                                      'result_approvals': result_approvals, 'count': count,
                                                      "to_deratify": to_deratify, "post_count": post_count,
                                                      'entity_approvals': entity_approvals})
    else:
        return render(request, 'no_access.html')


@login_required
def add_post_holder(request, pk):   # pk of the Post
    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        post_holder_Form = PostHolderForm(request.POST)
        if post_holder_Form.is_valid():
            email = post_holder_Form.cleaned_data['email']
            start_year = post_holder_Form.cleaned_data['session']

            try:
                name = User.objects.get(username=email)
                post.post_holders.add(name)
                session = Session.objects.filter(start_year=start_year).first()
                if session is None:
                    session = Session.objects.create(start_year=start_year)

                previous_history = PostHistory.objects.filter(post = post).filter(user = name).filter(post_session = session)

                if not previous_history:
                    PostHistory.objects.create(post=post, user=name, post_session=session,
                                             end=session_end_date(session.start_year))

                return HttpResponseRedirect(reverse('child_post', kwargs={'pk': pk}))



            except ObjectDoesNotExist:
                return render(request, 'add_post_holder.html', context={'post': post, 'form': post_holder_Form})

    else:
        post_holder_Form = PostHolderForm
        return render(request, 'add_post_holder.html', context={'post': post, 'form': post_holder_Form})



# view to create a new post, a child post for a post can be created only by the post holders of that post...
#is_safe
# parent is simply added ,goes directly to parent for approval
@login_required
def post_create(request, pk):
    parent = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post_form = PostForm(parent, request.POST)
        if post_form.is_valid():
            club_id = post_form.cleaned_data['club']
            club = Club.objects.get(pk=club_id)
            post = Post.objects.create(post_name=post_form.cleaned_data['post_name'], club=club, parent=parent,elder_brother= parent)
            post.take_approval = parent.parent
            post.post_approvals.add(parent.parent)
            post.save()
            return HttpResponseRedirect(reverse('post_view', kwargs={'pk': pk}))

    else:
        club = parent.club
        post_form = PostForm(parent)

    if request.user in parent.post_holders.all():
        return render(request, 'nomi/post_form.html', context={'form': post_form, 'parent': parent})
    else:
        return render(request, 'no_access.html')




@login_required
def senate_post_create(request, pk):
    parent = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post_form = PostForm(parent, request.POST)
        if post_form.is_valid():
            club_id = post_form.cleaned_data['club']
            club = Club.objects.get(pk=club_id)
            elder_brother_id = post_form.cleaned_data['elder_brother']
            elder_brother = Post.objects.get(pk=elder_brother_id)
            Post.objects.create(post_name=post_form.cleaned_data['post_name'],
                                elder_brother=elder_brother, club=club, parent=parent,
                                perms=post_form.cleaned_data['power'], status='Post approved')

            return HttpResponseRedirect(reverse('post_view', kwargs={'pk': pk}))

    else:
        club = parent.club
        post_form = PostForm(parent)

    if request.user in parent.post_holders.all():
        return render(request, 'nomi/post_form.html', context={'form': post_form, 'parent': parent})
    else:
        return render(request, 'no_access.html')


# only parent post have access to this view
# is_safe
@login_required
def child_post_view(request, pk):
    post = Post.objects.get(pk=pk)
    parent = post.parent
    nominations = Nomination.objects.filter(nomi_post=post)



    give_form = BlankForm(request.POST or None)
    if give_form.is_valid():
        if post.tag_perms == 'normal':
            post.tag_perms = 'Can create'
        else:
            post.tag_perms = 'normal'

        post.save()
        return HttpResponseRedirect(reverse('child_post', kwargs={'pk': pk}))

    if request.user in parent.post_holders.all():
        return render(request, 'child_post1.html', {'post': post, 'nominations': nominations, 'parent':parent,
                                                     'give_form': give_form})
    else:
        return render(request, 'no_access.html')

# the viewer_post which have access add its parent for approval of post and also add parent club as post tag..
# is_safe
@login_required
def post_approval(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    access = False
    if request.user in post.take_approval.post_holders.all():
        access = True


    if access:
        if post.take_approval.perms == "can ratify the post":
            post.status = 'Post approved'
            post.save()
            return HttpResponseRedirect(reverse('post_view', kwargs={'pk': post.take_approval.pk}))
        else:
            to_add = post.take_approval.parent
            current = post.take_approval
            post.post_approvals.add(to_add)
            post.tags.add(to_add.club)
            post.take_approval = to_add
            post.save()
            return HttpResponseRedirect(reverse('post_view', kwargs={'pk': current.pk}))
    else:
        return render(request, 'no_access.html')


def edit_post_name(request,post_pk):
    post = Post.objects.get(pk=post_pk)
    access = False
    if request.user in post.take_approval.post_holders.all():
        access = True

    if access:
        if request.method == 'POST':
            edit_post  = ChangePostName(request.POST)
            if edit_post.is_valid():
                post.post_name = edit_post.cleaned_data['post_name']
                post.save()
                return HttpResponseRedirect(reverse('edit_post_name', kwargs={'post_pk': post_pk}))


        else:
            edit_post = ChangePostName

        return render(request, 'edit_post_name.html', {'post': post,  'edit_post': edit_post})
    else:
        return render(request, 'no_access.html')




# the viewer removes himself from approvals ,thus delete the post down...
# is_safe
@login_required
def post_reject(request, post_pk):
    post = Post.objects.get(pk=post_pk)

    access = False
    if request.user in post.take_approval.post_holders.all():
        access = True
        view = post.take_approval


    if access:
        post.delete()
        return HttpResponseRedirect(reverse('post_view', kwargs={'pk': view.pk}))
    else:
        return render(request, 'no_access.html')

## ------------------------------------------------------------------------------------------------------------------ ##
#########################################    CLUB RELATED VIEWS   ######################################################
## ------------------------------------------------------------------------------------------------------------------ ##

# the viewer_post which have access add its parent for approval of club
# is_safe
@login_required
def club_approval(request, club_pk):
    club_create = ClubCreate.objects.get(pk=club_pk)
    access = False
    if request.user in club_create.take_approval.post_holders.all():
        access = True
        view = club_create.take_approval


    if access:
        if club_create.take_approval.perms == "can ratify the post":
            Club.objects.create(club_name = club_create.club_name,club_parent = club_create.club_parent)
            club_create.delete()
            return HttpResponseRedirect(reverse('post_view', kwargs={'pk': view.pk}))
        else:
            to_add = club_create.take_approval.parent
            club_create.take_approval = to_add
            club_create.save()
            return HttpResponseRedirect(reverse('post_view', kwargs={'pk': view.pk}))
    else:
        return render(request, 'no_access.html')

# the viewer removes himself from approvals ,thus delete the post down...
# is_safe
@login_required
def club_reject(request, club_pk):
    club_reject = ClubCreate.objects.get(pk=club_pk)

    access = False
    if request.user in club_reject.take_approval.post_holders.all():
        access = True
        view = club_reject.take_approval
        
    if access:
        club_reject.delete()

    return HttpResponseRedirect(reverse('post_view', kwargs={'pk': view.pk}))


## ------------------------------------------------------------------------------------------------------------------ ##
#########################################    NOMINATION RELATED VIEWS   ################################################
## ------------------------------------------------------------------------------------------------------------------ ##

# only post parent should create nomi...
# safe
@login_required
def nomination_create(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.parent.post_holders.all():
        if request.method == 'POST':
            title_form = NominationForm(request.POST)
            if title_form.is_valid():
                post = Post.objects.get(pk=pk)

                questionnaire = Questionnaire.objects.create(name=title_form.cleaned_data['title'])

                nomination = Nomination.objects.create(name=title_form.cleaned_data['title'],
                                                   description=title_form.cleaned_data['description'],
                                                   deadline=title_form.cleaned_data['deadline'],
                                                   nomi_session=title_form.cleaned_data['nomi_session'],
                                                   nomi_form=questionnaire, nomi_post=post,
                                                   )

                pk = questionnaire.pk
                return HttpResponseRedirect(reverse('forms:creator_form', kwargs={'pk': pk}))

        else:
            title_form = NominationForm()

        return render(request, 'nomi/nomination_form.html', context={'form': title_form, 'post': post})

    else:
        return render(request, 'no_access.html')




class NominationUpdate(UpdateView):
    model = Nomination
    fields = ['name', 'description']
    success_url = reverse_lazy('index')


class NominationDelete(DeleteView):
    model = Nomination
    success_url = reverse_lazy('index')


def nomi_replicate(request,nomi_pk):
    nomi_to_replicate = Nomination.objects.get(pk = nomi_pk)
    post = nomi_to_replicate.nomi_post
    if request.user in post.parent.post_holders.all():
        if request.method == 'POST':
            title_form = NominationReplicationForm(request.POST)
            if title_form.is_valid():
                questionnaire = replicate(nomi_to_replicate.nomi_form.pk)
                questionnaire.name = title_form.cleaned_data['title']
                questionnaire.save()

                nomination = Nomination.objects.create(name=title_form.cleaned_data['title'],
                                                       description=nomi_to_replicate.description,
                                                       deadline=title_form.cleaned_data['deadline'],
                                                       nomi_session=title_form.cleaned_data['nomi_session'],
                                                       nomi_form=questionnaire, nomi_post=post,
                                                       )

                pk = questionnaire.pk
                return HttpResponseRedirect(reverse('forms:creator_form', kwargs={'pk': questionnaire.pk}))

        else:
            title_form = NominationReplicationForm()

            return render(request, 'nomi/nomination_form.html', context={'form': title_form, 'post': post})

    else:
        return render(request, 'no_access.html')


# ****** in use...
def get_access_and_post(request,nomi_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    access = False
    view_post = None
    for post in nomi.nomi_approvals.all():
        if request.user in post.post_holders.all():
            access = True
            view_post = post
            break
    return access,view_post

def get_access_and_post_for_result(request, nomi_pk):
    nomi =Nomination.objects.get(pk=nomi_pk)
    access = False
    view_post = None
    for post in nomi.result_approvals.all():
        if request.user in post.post_holders.all():
            access = True
            view_post = post
            break
    return access, view_post


@login_required
def nomi_detail(request, nomi_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    parents = nomi.nomi_post.parent.post_holders.all()
    questionnaire = nomi.nomi_form
    form = questionnaire.get_form(request.POST or None)

    panelform = UserId(request.POST or None)

    access, view_post = get_access_and_post(request, nomi_pk)
    if not access:
        access, view_post = get_access_and_post_for_result(request, nomi_pk)

    status = [None]*7
    renomi_edit = 0
    p_in_rn = 0
    if nomi.status == 'Nomination created':
        status[0] = True
    elif nomi.status == 'Nomination out':
        status[1] = True
    elif nomi.status == 'Interview period':
        status[2] = True
    elif nomi.status == 'Sent for ratification':
        status[3] = True
    elif nomi.status == 'Interview period and Reopening initiated':
        status[4] = True
        if view_post in nomi.reopennomination.approvals.all():
            renomi_edit = 1
            if view_post.parent in nomi.reopennomination.approvals.all():
                p_in_rn = 1

    elif nomi.status == 'Interview period and Nomination reopened':
        status[5] = True
    else:
        status[6] = True


    if access:
        if view_post.perms == 'can approve post and send nominations to users' or view_post.perms == 'can ratify the post':
            power_to_send = 1
        else:
            power_to_send = 0
        if view_post.elder_brother in nomi.nomi_approvals.all():
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
                                                                  'panelists': panelists_exclude_parent,'renomi':renomi_edit,
                                                                  'p_in_rn':p_in_rn})


    elif request.user in nomi.interview_panel.all():
        return render(request, 'nomi_detail_user.html', context={'nomi': nomi})


    else:
        if status[1] or status[5]:
            return render(request, 'nomi_detail_user.html', context={'nomi': nomi})
        else:
            return render(request, 'no_access.html')

@login_required
def see_nomi_form(request, pk):
    nomi = Nomination.objects.get(pk=pk)
    if nomi.nomi_form and nomi.nomi_form.question_set.all():
        questionnaire = nomi.nomi_form
        form = questionnaire.get_form
        return render(request, 'see_nomi_form.html', context={'form': form, 'nomi':nomi })
    else:
        info = "There is not any form for this nomi"

        return render(request, 'nomi_done.html', context={'info': info})


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

    access, view_post = get_access_and_post(request, nomi_pk)

    if access:
        if view_post.elder_brother:
            to_add = view_post.elder_brother
            nomi.nomi_approvals.add(to_add)
            nomi.tags.add(view_post.parent.club)
            nomi.tags.add(to_add.club)

        else:
            to_add = view_post.parent
            nomi.nomi_approvals.add(to_add)
            nomi.tags.add(to_add.club)
        return HttpResponseRedirect(reverse('nomi_detail', kwargs={'nomi_pk': nomi_pk}))
    else:
        return render(request, 'no_access.html')


@login_required
def nomi_reject(request, nomi_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    access, view_post = get_access_and_post(request, nomi_pk)

    if access:
        to_remove = view_post
        nomi.nomi_approvals.remove(to_remove)
        return HttpResponseRedirect(reverse('post_view', kwargs={'pk': view_post.pk}))
    else:
        return render(request, 'no_access.html')


@login_required
def final_nomi_approval(request, nomi_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    access, view_post = get_access_and_post(request, nomi_pk)

    if access and (view_post.perms == "can ratify the post" or view_post.perms =="can approve post and send nominations to users") :
        if view_post.elder_brother:
            to_add = view_post.elder_brother
            nomi.nomi_approvals.add(to_add)
            nomi.tags.add(to_add.club)

        if view_post.parent:
            to_add = view_post.parent
            nomi.nomi_approvals.add(to_add)
            nomi.tags.add(to_add.club)

        nomi.open_to_users()
        return HttpResponseRedirect(reverse('nomi_detail', kwargs={'nomi_pk': nomi_pk}))
    else:
        return render(request, 'no_access.html')


@login_required
def copy_nomi_link(request, pk):
    url = DOMAIN_NAME + '/nominations/nomi_detail/' + str(pk) + '/'
    pyperclip.copy(url)

    return HttpResponseRedirect(reverse('admin_portal'))



## ------------------------------------------------------------------------------------------------------------------ ##
#########################################   REOPEN NOMINATION MONITOR VIEWS   ##########################################
## ------------------------------------------------------------------------------------------------------------------ ##


@login_required
def reopen_nomi(request, nomi_pk):
    access , view_post = get_access_and_post(request,nomi_pk)
    nomi = Nomination.objects.get(pk=nomi_pk)
    if access:
        re_nomi = ReopenNomination.objects.create(nomi=nomi)
        re_nomi.approvals.add(view_post)
        if view_post.elder_brother:
            re_nomi.approvals.add(view_post.elder_brother)
        re_nomi.nomi.status = 'Interview period and Reopening initiated'
        re_nomi.nomi.save()
        return HttpResponseRedirect(reverse('nomi_detail', kwargs={'nomi_pk': nomi_pk}))
    else:
        return render(request, 'no_access.html')


# ****** in use...
def get_access_and_post_for_renomi(request,re_nomi_pk):
    re_nomi = ReopenNomination.objects.get(pk=re_nomi_pk)
    access = False
    view_post = None
    for post in re_nomi.approvals.all():
        if request.user in post.post_holders.all():
            access = True
            view_post = post
            break
    return access,view_post


@login_required
def re_nomi_approval(request, re_nomi_pk):
    re_nomi = ReopenNomination.objects.get(pk=re_nomi_pk)
    access , view_post = get_access_and_post_for_renomi(request,re_nomi_pk)

    if access:
        if view_post.perms == "can ratify the post" or view_post.perms =="can approve post and send nominations to users":
            re_nomi.re_open_to_users()
            nomi = re_nomi.nomi
            re_nomi.delete()
            return HttpResponseRedirect(reverse('nomi_detail', kwargs={'nomi_pk': nomi.pk}))
        else:
            to_add = view_post.elder_brother
            re_nomi.approvals.add(to_add)
            return HttpResponseRedirect(reverse('nomi_detail', kwargs={'nomi_pk': re_nomi.nomi.pk}))
    else:
        return render(request, 'no_access.html')


@login_required
def re_nomi_reject(request, re_nomi_pk):
    re_nomi = ReopenNomination.objects.get(pk=re_nomi_pk)
    access , view_post = get_access_and_post_for_renomi(request,re_nomi_pk)
    if access:
        nomi = re_nomi.nomi
        nomi.status = 'Interview period'
        nomi.save()
        re_nomi.delete()
        return HttpResponseRedirect(reverse('nomi_detail', kwargs={'nomi_pk': nomi.pk}))
    else:
        return render(request, 'no_access.html')


@login_required
def final_re_nomi_approval(request, re_nomi_pk):
    re_nomi = ReopenNomination.objects.get(pk=re_nomi_pk)
    access , view_post = get_access_and_post_for_renomi(request,re_nomi_pk)

    if access:
        re_nomi.re_open_to_users()
        nomi=re_nomi.nomi
        re_nomi.delete()
        return HttpResponseRedirect(reverse('nomi_detail', kwargs={'nomi_pk': nomi.pk}))
    else:
        return render(request, 'no_access.html')


## ------------------------------------------------------------------------------------------------------------------ ##
#########################################    NOMINATION MONITOR VIEWS   ################################################
## ------------------------------------------------------------------------------------------------------------------ ##
# ****** in use...


@login_required
def nomi_apply(request, pk):
    nomination = Nomination.objects.get(pk=pk)
    count = NominationInstance.objects.filter(nomination=nomination).filter(user=request.user).count()

    if not count and (nomination.status == "Nomination out" or nomination.status =="Interview period and Nomination reopened"):
        if nomination.nomi_form:
            questionnaire = nomination.nomi_form
            form = questionnaire.get_form(request.POST or None)
            form_confirm = SaveConfirm(request.POST or None)

            if form_confirm.is_valid():
                if form.is_valid():
                    filled_form = questionnaire.add_answer(request.user, form.cleaned_data)
                    if form_confirm.cleaned_data["save_or_submit"] == "only save":
                        NominationInstance.objects.create(user=request.user, nomination=nomination,
                                                          filled_form=filled_form,
                                                          submission_status=False, timestamp=date.today())
                        info = "Your application has been saved. It has not been submited. So make sure you submit it after further edits through your profile module"

                    else:
                        NominationInstance.objects.create(user=request.user, nomination=nomination, filled_form=filled_form,
                                                      submission_status = True,timestamp = date.today())
                        info = "Your application has been recorded. You can edit it through profile module."

                    return render(request, 'nomi_done.html', context={'info': info})

            return render(request, 'forms/show_form.html', context={'form': form, 'form_confirm': form_confirm,
                                                                    'questionnaire': questionnaire, 'pk': pk})
        else:
            form_confirm = ConfirmApplication(request.POST or None)

            if form_confirm.is_valid():
                NominationInstance.objects.create(user=request.user, nomination=nomination,submission_status = True,timestamp = date.today())
                info = "Your application has been recorded."
                return render(request, 'nomi_done.html', context={'info': info})

    else:
        info = "You have applied for it already.You can edit it through profile module."

        if not (nomination.status == "Nomination out" or nomination.status =="Interview period and Nomination reopened"):
            info =  "Nomination has been closed"
        return render(request, 'nomi_done.html', context={'info': info})




def nomi_answer_edit(request, pk):
    application = NominationInstance.objects.get(pk=pk)
    nomination = application.nomination

    if application.user == request.user and (nomination.status == "Nomination out" or nomination.status =="Interview period and Nomination reopened") :
        ans_form = application.filled_form
        data = json.loads(ans_form.data)
        applicant = application.user.userprofile
        questionnaire = application.nomination.nomi_form
        form = questionnaire.get_form(request.POST or data)

        if nomination.nomi_form and application.submission_status== False:
            form_confirm = SaveConfirm(request.POST or None)
            if form_confirm.is_valid():
                if form.is_valid():
                    info = "Your application has been edited and saved locally. Don't forget to submit it before deadline "
                    if form_confirm.cleaned_data["save_or_submit"] == "save and submit":
                        application.submission_status = True
                        application.timestamp = date.today()
                        application.save()
                        info = "Your application has been edited and finally submitted."

                    json_data = json.dumps(form.cleaned_data)
                    ans_form.data = json_data
                    ans_form.save()
                    application.edit_time = date.today()
                    application.save()

                    return render(request, 'nomi_done.html', context={'info': info})


        else:
            form_confirm = ConfirmApplication(request.POST or None)


        if form_confirm.is_valid():
            if form.is_valid():
                json_data = json.dumps(form.cleaned_data)
                ans_form.data = json_data
                ans_form.save()
                application.edit_time = date.today()
                application.save()

                info = "Your application has been edited"
                return render(request, 'nomi_done.html', context={'info': info})

        return render(request, 'nomi_answer_edit.html', context={'form': form, 'form_confirm': form_confirm,
                                                                 'nomi': application, 'nomi_user': applicant})
    else:
        return render(request, 'no_access.html')


def get_mails(query_users):
    mail_ids = ''
    for each in query_users:
        if len(mail_ids):
            mail_ids = mail_ids + ', ' + str(each.user) + '@iitk.ac.in'
        else:
            mail_ids = str(each.user) + '@iitk.ac.in'

    return mail_ids

def get_nomi_status(nomination):
    status = [None] * 7

    if nomination.status == 'Nomination created':
        status[0] = True
    elif nomination.status == 'Nomination out':
        status[1] = True
    elif nomination.status == 'Interview period':
        status[2] = True
    elif nomination.status == 'Sent for ratification':
        status[3] = True
    elif nomination.status == 'Interview period and Reopening initiated':
        status[4] = True
    elif nomination.status == 'Interview period and Nomination reopened':
        status[5] = True
    else:
        status[6] = True

    return status

def get_accepted_csv(request,nomi_pk):
    # Create the HttpResponse object with the appropriate CSV header.
    nomination = Nomination.objects.get(pk=nomi_pk)
    accepted = NominationInstance.objects.filter(nomination=nomination).filter(status='Accepted')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="accepted.csv"'

    writer = csv.writer(response)

    writer.writerow([str(nomination.name),'SELECTED APPLICANTS', str(date.today())])
    writer.writerow(['S.No','Name', 'Email','Roll','Address','Contact'])
    i=1
    for each in accepted:
        try :
            profile = each.user.userprofile
            writer.writerow([str(i),each.user.userprofile,str(each.user)+'@iitk.ac.in',str(profile.roll_no),str(profile.room_no)+'/'+ str(profile.hall),str(profile.contact)])
        except:
            writer.writerow([str(i),each.user,str(each.user)+'@iitk.ac.in',str(each.start)])


        i = i + 1

    return response

@login_required
def applications(request, pk):
    nomination = Nomination.objects.get(pk=pk)
    applicants = NominationInstance.objects.filter(nomination=nomination).filter(submission_status = True)
    accepted = NominationInstance.objects.filter(nomination=nomination).filter(submission_status = True).filter(status='Accepted')
    rejected = NominationInstance.objects.filter(nomination=nomination).filter(submission_status = True).filter(status='Rejected')
    pending = NominationInstance.objects.filter(nomination=nomination).filter(submission_status = True).filter(status=None)

    mail_ids = [get_mails(applicants),get_mails(accepted),get_mails(rejected),get_mails(pending)]


    status = get_nomi_status(nomination)

    access, view_post = get_access_and_post_for_result(request, pk)
    if not access:
        access, view_post = get_access_and_post(request, pk)


    # if user post in parent tree
    if access:
        permission = None
        senate_permission = None

        if view_post.parent:
            if view_post.parent.perms == 'can ratify the post':
                permission = True
                senate_permission = False
        elif view_post.perms == 'can ratify the post':
            senate_permission = True
            permission = False

        # result approval things    can send,has been sent, can cancel
        results_approval = [None]*3

        if view_post in nomination.result_approvals.all():
            if view_post.parent in nomination.result_approvals.all():
                results_approval[1] = True
                grand_parent = view_post.parent.parent
                if grand_parent not in nomination.result_approvals.all():
                    results_approval[2] = True
            else:
                results_approval[0] = True


        if request.method == 'POST':
            reopen = DeadlineForm(request.POST)
            if reopen.is_valid():
                re_nomi = ReopenNomination.objects.create(nomi=nomination)
                re_nomi.approvals.add(view_post)
                nomination.deadline = reopen.cleaned_data['deadline']
                nomination.status = 'Interview period and Reopening initiated'
                nomination.save()
                return HttpResponseRedirect(reverse('nomi_detail', kwargs={'nomi_pk': pk}))
        else:
            reopen = DeadlineForm()



        form_confirm = ConfirmApplication(request.POST or None)
        if form_confirm.is_valid():
            nomination.status = 'Interview period'
            nomination.save()
            return HttpResponseRedirect(reverse('applicants', kwargs={'pk': pk}))



        return render(request, 'applicants.html', context={'nomination': nomination, 'applicants': applicants,
                                                           'form_confirm': form_confirm,'mail_ids':mail_ids,
                                                           'result_approval': results_approval,
                                                           'accepted': accepted, 'rejected': rejected, 'status': status,
                                                           'pending': pending, 'perm': permission,
                                                           'senate_perm': senate_permission,'reopen':reopen})



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

    nomination = application.nomination
    status = get_nomi_status(nomination)

    access = False
    access, view_post = get_access_and_post(request, nomination.pk)
    if not access:
        access, view_post = get_access_and_post_for_result(request, nomination.pk)

    all_posts = Post.objects.filter(post_holders=request.user)
    senate_perm = False
    for post in all_posts:
        if post.perms == 'can ratify the post':
            access = True
            senate_perm = True
            break



    if application.user == request.user:
        return render(request, 'nomi_answer_user.html', context={'form': form, 'nomi': application, 'nomi_user': applicant})




    if access or request.user in nomination.interview_panel.all():

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
                                                            'comment_form': comment_form,
                                                            'comments': comments_reverse, 'senate_perm': senate_perm,
                                                             'status':status,
                                                            'result_approval': results_approval})
    else:
        return render(request, 'no_access.html')





## ------------------------------------------------------------------------------------------------------------------ ##
#########################################     GROUP NOMINATION VIEWS    ################################################
## ------------------------------------------------------------------------------------------------------------------ ##


@login_required
def group_nominations(request, pk):
    post = Post.objects.get(pk=pk)
    child_posts = Post.objects.filter(parent=post)
    child_posts_reverse = child_posts[::-1]
    post_approvals = Post.objects.filter(post_approvals=post).filter(status='Post created')
    nomi_approvals = Nomination.objects.filter(nomi_approvals=post).filter(status='Nomination created')

    if request.user in post.post_holders.all():
        if request.method == 'POST':
            groupform = SelectNomiForm(post, request.POST)
            group_detail = GroupDetail(request.POST)
            if group_detail.is_valid():
                if groupform.is_valid():
                    group = group_detail.save()
                    group.approvals.add(post)
                    for nomi_pk in groupform.cleaned_data['group']:
                        # tasks to be performed on nomination
                        nomi = Nomination.objects.get(pk=nomi_pk)
                        group.nominations.add(nomi)
                        for tag in nomi.tags.all():
                            group.tags.add(tag)
                        nomi.group_status = 'grouped'
                        if post.elder_brother:
                            to_add = post.elder_brother
                            nomi.nomi_approvals.add(to_add)
                        if group.deadline:
                            nomi.deadline = group.deadline
                        nomi.save()
                    return HttpResponseRedirect(reverse('post_view', kwargs={'pk': pk}))

        else:
            group_detail= GroupDetail
            groupform = SelectNomiForm(post)

        return render(request, 'nomi_group.html', context={'post': post, 'child_posts': child_posts_reverse,
                                                           'post_approval': post_approvals, 'nomi_approval': nomi_approvals,
                                                           'form': groupform, 'title_form': group_detail})
    else:
        return render(request, 'no_access.html')


@login_required
def group_nomi_detail(request, pk):
    group_nomi = GroupNomination.objects.get(pk=pk)
    admin = 0
    for post in request.user.posts.all():
        if post in group_nomi.approvals.all():
            admin = post

    form_confirm = ConfirmApplication(request.POST or None)
    if form_confirm.is_valid():
        for nomi in group_nomi.nominations.all():
            nomi.open_to_users()
        group_nomi.status = 'out'
        group_nomi.save()

    return render(request, 'group_detail.html', {'group_nomi': group_nomi, 'admin': admin,
                                                 'form_confirm': form_confirm})


@login_required
def edit_or_add_to_group(request, pk, gr_pk):
    post = Post.objects.get(pk=pk)
    group = GroupNomination.objects.get(pk=gr_pk)

    if request.user in post.post_holders.all() and post in group.approvals.all():
        group_detail = GroupDetail(request.POST or None, instance=group)
        if group_detail.is_valid():
            group_detail.save()
        if request.method == 'POST':
            groupform = SelectNomiForm(post, request.POST)

            if groupform.is_valid():

                for nomi_pk in groupform.cleaned_data['group']:
                    # things to be performed on nomination
                    nomi = Nomination.objects.get(pk=nomi_pk)
                    group.nominations.add(nomi)
                    for tag in nomi.tags.all():
                        group.tags.add(tag)
                    nomi.group_status = 'grouped'
                    if post.elder_brother:
                        to_add = post.elder_brother
                        nomi.nomi_approvals.add(to_add)
                    if group.deadline:
                        nomi.deadline = group.deadline

                    nomi.save()
                return HttpResponseRedirect(reverse('group_nomi_detail', kwargs={'pk': gr_pk}))

        else:
            groupform = SelectNomiForm(post)

        return render(request, 'nomi_group.html', context={'post': post,'form': groupform, 'title_form': group_detail})
    else:
        return render(request, 'no_access.html')



@login_required
def remove_from_group(request, nomi_pk, gr_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    group = GroupNomination.objects.get(pk=gr_pk)
    group.nominations.remove(nomi)

    nomi.group_status = 'normal'
    nomi.status = 'Nomination created'
    nomi.save()

    return HttpResponseRedirect(reverse('group_nomi_detail', kwargs={'pk': gr_pk}))



## ------------------------------------------------------------------------------------------------------------------ ##
###########################################    RATIFICATION VIEWS    ###################################################
## ------------------------------------------------------------------------------------------------------------------ ##


@login_required
def ratify(request, nomi_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    access, view_post = get_access_and_post_for_result(request,nomi_pk)

    if access:
        if  view_post.perms == "can ratify the post":
            nomi.append()
            return HttpResponseRedirect(reverse('applicants', kwargs={'pk': nomi_pk}))
        else:
            return render(request, 'no_access.html')
    else:
        return render(request, 'no_access.html')


@login_required
def request_ratify(request, nomi_pk):
    nomi = Nomination.objects.get(pk=nomi_pk)
    access, view_post = get_access_and_post_for_result(request,nomi_pk)

    if access:
        if view_post.parent:
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
    access, view_post = get_access_and_post_for_result(request,nomi_pk)

    if access:
        if view_post.parent:
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
    access, view_post = get_access_and_post_for_result(request,nomi_pk)

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
    access, view_post = get_access_and_post_for_result(request,nomi_pk)

    if access:
        if view_post == nomi.nomi_post.parent:
            nomi.show_result = True

        to_add = view_post.parent
        nomi.result_approvals.add(to_add)
        return HttpResponseRedirect(reverse('applicants', kwargs={'pk': nomi_pk}))
    else:
        return render(request, 'no_access.html')

@login_required
def create_deratification_request(request, post_pk, user_pk):
    post = Post.objects.get(pk=post_pk)
    user =User.objects.get(pk=user_pk)

    if request.user in post.parent.post_holders.all():
        Deratification.objects.create(name=user, post=post,status = 'requested', deratify_approval=post.parent)


    return HttpResponseRedirect(reverse('child_post', kwargs={'pk': post_pk}))


@login_required
def approve_deratification_request(request,pk):
    to_deratify = Deratification.objects.get(pk = pk)
    view = to_deratify.deratify_approval
    if request.user in view.post_holders.all():
        if view.perms == "can ratify the post":
             to_deratify.post.post_holders.remove(to_deratify.name)
             history=PostHistory.objects.filter(user=to_deratify.name).filter(post = to_deratify.post)
             history.delete()
             to_deratify.status = 'deratified'
             to_deratify.save()

        else:
            to_deratify.deratify_approval = view.parent
            to_deratify.save()

        return HttpResponseRedirect(reverse('post_view', kwargs={'pk':view.pk}))
    else:
        return render(request, 'no_access.html')




@login_required
def reject_deratification_request(request, pk):
    to_deratify = Deratification.objects.get(pk=pk)
    view = to_deratify.deratify_approval
    if request.user in view.post_holders.all():
        to_deratify.delete()
        return HttpResponseRedirect(reverse('post_view', kwargs={'pk':view.pk}))
    else:
        return render(request, 'no_access.html')



'''
mark_as_interviewed, reject_nomination, accept_nomination: Changes the interview status/ nomination_instance status
of the applicant
'''

def get_access_and_post_for_selection(request, nomi_pk):
    nomi =Nomination.objects.get(pk=nomi_pk)
    access = False
    view_post = None
    for post in nomi.result_approvals.all():
        if request.user in post.post_holders.all():
            access = True
            view_post = post
            break

    return access, view_post

@login_required
def mark_as_interviewed(request, pk):

    application = NominationInstance.objects.get(pk=pk)
    id_nomi = application.nomination.pk
    nomination = Nomination.objects.get(pk=id_nomi)
    access, view_post = get_access_and_post_for_selection(request,id_nomi)
    if access or request.user in nomination.interview_panel.all():
        application.interview_status = 'Interview Done'
        application.save()
        return HttpResponseRedirect(reverse('nomi_answer', kwargs={'pk': pk}))
    else:
        return render(request, 'no_access.html')


@login_required
def accept_nomination(request, pk):
    application = NominationInstance.objects.get(pk=pk)
    id_accept = application.nomination.pk
    nomination = Nomination.objects.get(pk=id_accept)
    access, view_post = get_access_and_post_for_selection(request, id_accept)
    if access or request.user in nomination.interview_panel.all():
        application.status = 'Accepted'
        application.save()

        comment = '<strong>' + str(request.user.userprofile.name) + '</strong>' + ' Accepted '\
                  + '<strong>' + str(application.user.userprofile.name) + '</strong>'
        status = Commment.objects.create(comments=comment, nomi_instance=application)

        return HttpResponseRedirect(reverse('applicants', kwargs={'pk': id_accept}))
    else:
        return render(request, 'no_access.html')




@login_required
def reject_nomination(request, pk):
    application = NominationInstance.objects.get(pk=pk)
    id_reject = application.nomination.pk
    nomination = Nomination.objects.get(pk=id_reject)
    access, view_post = get_access_and_post_for_selection(request, id_reject)
    if access or request.user in nomination.interview_panel.all():
        application.status = 'Rejected'
        application.save()

        comment = '<strong>' + str(request.user.userprofile.name) + '</strong>' + ' Rejected ' \
                  + '<strong>' + str(application.user.userprofile.name) + '</strong>'
        status = Commment.objects.create(comments=comment, nomi_instance=application)

        return HttpResponseRedirect(reverse('applicants', kwargs={'pk': id_reject}))
    else:
        return render(request, 'no_access.html')


'''
append_user, replace_user: Adds and Removes the current post-holders according to their selection status
'''

@login_required
def append_user(request, pk):
    posts = request.user.posts.all()
    access = False
    for post in posts:
        if post.perms == "can ratify the post":
            access = True
            break

    if access:
        nomi = Nomination.objects.get(pk=pk)
        nomi.append()
        return HttpResponseRedirect(reverse('applicants', kwargs={'pk': pk}))
    else:
        return render(request, 'no_access.html')



@login_required
def end_tenure(request):
    posts = Post.objects.all()

    for post in posts:
        for holder in post.post_holders.all():
            try:
                history = PostHistory.objects.get(post=post, user=holder)

                if datetime.now() > history.end:
                    post.post_holders.remove(holder)

            except ObjectDoesNotExist:
                return HttpResponseRedirect(reverse('index'))

    return HttpResponseRedirect(reverse('index'))

    # Import all posts of all clubs
    # Check if their session has expired (31-3-2018 has passed)
    # Remove them from the post
    # Create the post history (No need, its already created)

## ------------------------------------------------------------------------------------------------------------------ ##
############################################       PROFILE VIEWS      ##################################################
## ------------------------------------------------------------------------------------------------------------------ ##


@login_required
def profile_view(request):
    pk = request.user.pk

    my_posts = Post.objects.filter(post_holders=request.user)
    history = PostHistory.objects.filter(user=request.user).order_by('start')

    pending_nomi = NominationInstance.objects.filter(user=request.user).filter(nomination__status='Nomination out')
    pending_re_nomi = NominationInstance.objects.filter(user=request.user).\
        filter(nomination__status='Interview period and Nomination reopened')
    pending_nomi = pending_nomi | pending_re_nomi

    # show the instances that user finally submitted.. not the saved one
    interview_re_nomi = NominationInstance.objects.filter(user=request.user).filter(submission_status = True).filter(nomination__status='Interview period and Reopening initiated')
    interview_nomi = NominationInstance.objects.filter(user=request.user).filter(submission_status = True).filter(nomination__status='Interview period')

    interview_nomi = interview_nomi | interview_re_nomi

    declared_nomi = NominationInstance.objects.filter(user=request.user).filter(submission_status = True).filter(nomination__status='Sent for ratification')


    try:
        user_profile = UserProfile.objects.get(user__id=pk)
        post_exclude_history = []    # In case a post is not registered in history

        post_history = []
        for his in history:
            post_history.append(his.post)

        for post in my_posts:
            if post not in post_history:
                post_exclude_history.append(post)

        return render(request, 'profile.html', context={'user_profile': user_profile, 'history': history,
                                                        'pending_nomi': pending_nomi, 'declared_nomi': declared_nomi,
                                                        'interview_nomi': interview_nomi, 'my_posts': my_posts,
                                                        'excluded_posts': post_exclude_history})

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



class UserProfileUpdate(UpdateView):
    model = UserProfile
    fields = ['user_img', 'hall', 'room_no', 'contact']
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


def all_nominations(request):
    all_nomi = Nomination.objects.all().exclude(status='Nomination created')

    return render(request, 'all_nominations.html', context={'all_nomi': all_nomi})



