from django.shortcuts import render
from nomi.models import UserProfile
from .filters import UserProfileFilter


def index(request):
    user_list = UserProfileFilter(request.GET, queryset=UserProfile.objects.all().order_by('name'))

    return render(request, 'index.html', context={'filter': user_list})
