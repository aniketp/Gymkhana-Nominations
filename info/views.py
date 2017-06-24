from django.shortcuts import render
from nomi.models import Post
from info.filters import PostFilter


def index(request):
    user_list = PostFilter(request.GET, queryset=Post.objects.all().order_by('post_name').distinct())

    return render(request, 'index.html', context={'filter': user_list})
