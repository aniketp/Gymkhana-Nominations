from django.shortcuts import render,HttpResponse
import csv

from nomi.models import *
from info.forms import ClubForm, PostForm, SessionForm,current_session
from django.contrib.auth.decorators import login_required
from info.forms import ClubForm, PostForm, SessionForm, current_session
from nomi.forms import BlankForm



def get_mail(query_users):
    mail_ids = ''
    for each in query_users:
        if len(mail_ids):
            mail_ids = mail_ids + ', ' + str(each.user) + '@iitk.ac.in'
        else:
            mail_ids = str(each.user) + '@iitk.ac.in'

    return mail_ids


def get_csv(request,session_pk,club_pk,post_pk):
    # Create the HttpResponse object with the appropriate CSV header.
    query = PostHistory.objects.none()
    session = Session.objects.get(pk= session_pk)

    if club_pk == 'NA':
        query = PostHistory.objects.filter(post_session=session)
    else:
        if post_pk == 'NA':
            club =Club.objects.get(pk =club_pk)
            query_posts = club.club_posts.all()
            for each in query_posts:
                post_user = PostHistory.objects.filter(post_session=session).filter(post=each)
                query = query | post_user
        else:
            post = Post.objects.get(pk=post_pk)
            query = PostHistory.objects.filter(post_session=session, post=post)



    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="post_holders.csv"'

    writer = csv.writer(response)

    writer.writerow(['S.No', 'Post', 'Name', 'Email','Ratified on','Roll','Address','Contact'])
    i=1
    for each in query:
        try :
            profile = each.user.userprofile
            writer.writerow([str(i),each.post,each.user.userprofile,str(each.user)+'@iitk.ac.in',str(each.start),str(profile.roll_no),str(profile.room_no)+'/'+ str(profile.hall),str(profile.contact)])
        except:
            writer.writerow([str(i),each.post,each.user,str(each.user)+'@iitk.ac.in',str(each.start)])


        i = i + 1

    return response


@login_required
def post_holder_search(request):
    club = None
    session = current_session()
    query_posts = None
    query_users = PostHistory.objects.none()

    get_ids = BlankForm(request.POST or None)


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
                    set = [session.pk,'NA','NA']
                    return render(request, 'info.html',
                                  context={'club_form': club_form, 'post_form': post_form, 'session_form': session_form,
                                           'query_users': query_users ,'get_ids':get_ids,'set':set})

                club = Club.objects.get(pk=club_form.cleaned_data['club'])

                if post_form.is_valid():
                    post = Post.objects.get(pk=post_form.cleaned_data['post'], tags=club)
                    query_posts = post
                    post_form = PostForm(club)
                    query_users = PostHistory.objects.filter(post_session=session , post = query_posts)

                    get_ids = get_mail(query_users)
                    set = [session.pk,club.pk,post.pk]

                    return render(request, 'info.html',
                              context={'club_form': club_form, 'post_form': post_form,'session_form':session_form,
                                       'query_users': query_users,'get_ids':get_ids,'set':set})

                post_form = PostForm(club)
                query_posts = club.club_posts.all()
                for each in query_posts:
                    post_user = PostHistory.objects.filter(post_session = session).filter(post = each)
                    query_users = query_users|post_user

                get_ids = get_mail(query_users)
                set = [session.pk, club.pk, 'NA']

                return render(request, 'info.html',
                          context={'club_form': club_form, 'post_form': post_form,'session_form':session_form,
                                   'query_users': query_users,'get_ids':get_ids,'set':set})



    else:
        club_form = ClubForm
        post_form = None
        session_form = SessionForm(initial={'year': session.id})
        query_users = PostHistory.objects.filter(post_session = session)
        get_ids = get_mail(query_users)
        set=[session.pk,'NA','NA']

    return render(request, 'info.html', context={'club_form': club_form, 'post_form': post_form,'session_form':session_form,
                                                  'query_users': query_users,'get_ids':get_ids,'set':set})


