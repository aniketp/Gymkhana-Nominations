from django.shortcuts import render
from .models import Nomination,NominationInstance
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.auth.decorators import login_required ,permission_required
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User



def index(request):
    nominations = Nomination.objects.all()
    all_nominations = nominations[::-1]

    return render(request, 'index.html', context={'all_nominations': all_nominations})


@login_required
def nomi_apply(request,pk):
    nomination = Nomination.objects.get(pk=pk)
    Ins = NominationInstance.objects.create(user=request.user,nomination=nomination)
    return render(request,'nomi_done.html', context={'nomi':nomination})


