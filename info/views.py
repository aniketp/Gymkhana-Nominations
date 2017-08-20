from django.shortcuts import render

from nomi.models import *
from info.forms import ClubForm, PostForm, SessionForm,current_session
from django.contrib.auth.decorators import login_required
from info.forms import ClubForm, PostForm, SessionForm, current_session
from nomi.forms import BlankForm

def index(request):
    club = None
    query_posts = None

    if request.method == 'POST':
        club_form = ClubForm(request.POST)
        post_form = PostForm(club, request.POST)

        if club_form.is_valid():
            club = Club.objects.get(pk=club_form.cleaned_data['club'])

            if post_form.is_valid():
                post = Post.objects.filter(pk=post_form.cleaned_data['post'], tags=club)
                query_posts = post
                post_form = PostForm(club)
                return render(request, 'index.html',
                              context={'club_form': club_form, 'post_form': post_form,
                                       'query_posts': query_posts})

            post_form = PostForm(club)
            query_posts = club.club_posts.all()
            return render(request, 'index.html',
                          context={'club_form': club_form, 'post_form': post_form,
                                   'query_posts': query_posts})

    else:
        club_form = ClubForm
        post_form = None
        query_posts = Post.objects.all()

    return render(request, 'index.html', context={'club_form': club_form, 'post_form': post_form,
                                                  'query_posts': query_posts})


def get_mail(query_users):
    mail_ids = ''
    for each in query_users:
        if len(mail_ids):
            mail_ids = mail_ids + ', ' + str(each.user) + '@iitk.ac.in'
        else:
            mail_ids = str(each.user) + '@iitk.ac.in'

    return mail_ids


@login_required
def post_holder_search(request):
    club = None
    session = current_session()
    query_posts = None
    query_users = PostHistory.objects.none()

    get_ids = BlankForm(request.POST or None)
    status = None

    if request.method == 'POST':
        session_form = SessionForm(request.POST)
        club_form = ClubForm(request.POST)
        post_form = PostForm(club, request.POST)

        if session_form.is_valid():
            session = Session.objects.get(pk=session_form.cleaned_data['year'])


            if club_form.is_valid():

                if club_form.cleaned_data['club'] == 'NA':
                    club_form = ClubForm
                    post_form = None
                    query_users = PostHistory.objects.filter(post_session=session)
                    get_ids = get_mail(query_users)
                    return render(request, 'info.html',
                                  context={'club_form': club_form, 'post_form': post_form, 'session_form': session_form,
                                           'query_users': query_users ,'get_ids':get_ids})

                club = Club.objects.get(pk=club_form.cleaned_data['club'])

                if post_form.is_valid():
                    post = Post.objects.filter(pk=post_form.cleaned_data['post'], tags=club)
                    query_posts = post
                    post_form = PostForm(club)
                    query_users = PostHistory.objects.filter(post_session=session , post = query_posts)

                    get_ids = get_mail(query_users)

                    return render(request, 'info.html',
                              context={'club_form': club_form, 'post_form': post_form,'session_form':session_form,
                                       'query_users': query_users,'get_ids':get_ids})

                post_form = PostForm(club)
                query_posts = club.club_posts.all()
                session_user = PostHistory.objects.filter(post_session = session)
                for each in query_posts:
                    post_user = PostHistory.objects.filter(post_session = session).filter(post = each)
                    query_users = query_users|post_user

                get_ids = get_mail(query_users)

                return render(request, 'info.html',
                          context={'club_form': club_form, 'post_form': post_form,'session_form':session_form,
                                   'query_users': query_users,'get_ids':get_ids})



    else:
        club_form = ClubForm
        post_form = None
        session_form = SessionForm(initial={'year': session.id})
        query_users = PostHistory.objects.filter(post_session = session)
        get_ids = get_mail(query_users)

    return render(request, 'info.html', context={'club_form': club_form, 'post_form': post_form,'session_form':session_form,
                                                  'query_users': query_users,'get_ids':get_ids})



