from django.shortcuts import render
from .models import Nomination


def index(request):
    nominations = Nomination.objects.all()
    all_nominations = nominations[::-1]

    return render(request, 'index.html', context={'all_nominations': all_nominations})


