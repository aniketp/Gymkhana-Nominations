from django.shortcuts import render
from nomi.models import Post,Club
from info.forms import ClubForm,PostForm


def index(request):
    club = None

    if request.method == 'POST':
        club_form = ClubForm(request.POST)
        post_form = PostForm(club,request.POST)


        if club_form.is_valid():
            club = Club.objects.get(pk = club_form.cleaned_data['club'])

            if post_form.is_valid():
                post = Post.objects.filter(pk=post_form.cleaned_data['post'],tag = club)
                query_posts = post
                post_form = PostForm(club)
                return render(request, 'index.html',
                              context={'club_form': club_form, 'post_form': post_form,
                                       'query_posts': query_posts})

            post_form = PostForm(club)
            query_posts = club.club_posts.all()
            return render(request, 'index.html',
                          context={'club_form': club_form,'post_form':post_form ,
                                   'query_posts': query_posts})


    else:
        club_form = ClubForm
        post_form = None
        query_posts = Post.objects.all()

    return render(request, 'index.html', context={'club_form':club_form,'post_form':post_form,
                                                  'query_posts':query_posts})
