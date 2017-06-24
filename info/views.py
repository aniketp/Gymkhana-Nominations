from django.shortcuts import render
from nomi.models import Post,Club
from info.filters import PostFilter


def index(request):
    user_list = PostFilter(request)

    return render(request, 'index.html', context={'filter': user_list})
