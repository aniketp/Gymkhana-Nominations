from django.shortcuts import render
from .models import Nomination,NominationInstance
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.auth.decorators import login_required ,permission_required
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User



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


