from django.shortcuts import render
from .models import Nomination, NominationInstance
from django.contrib.auth.decorators import login_required ,permission_required
from django.views import generic


def index(request):
    nominations = Nomination.objects.all()
    all_nominations = nominations[::-1]

    return render(request, 'index.html', context={'all_nominations': all_nominations})


@login_required
def nomi_apply(request, pk):
    nomination = Nomination.objects.get(pk=pk)
    ct=NominationInstance.objects.filter(nomination=nomination).filter(user=request.user).count()
    if not ct:
         Ins = NominationInstance.objects.create(user=request.user, nomination=nomination)
         info = "Your application has been recorded"
         return render(request, 'nomi_done.html', context={'info': info})
    else:
        info = "You have applied for it already."

    return render(request, 'nomi_done.html', context={'info': info})


def result(request, pk):
    nomination = Nomination.objects.get(pk=pk)
    users = NominationInstance.objects.filter(nomination=nomination).filter(status__exact='a')

    return render(request, 'result.html', context={'users': users})
