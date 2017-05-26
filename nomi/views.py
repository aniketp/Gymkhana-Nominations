from django.shortcuts import render
from .models import Nomination, NominationInstance, UserProfile
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy


def index(request):
    nominations = Nomination.objects.all()
    all_nominations = nominations[::-1]

    return render(request, 'index.html', context={'all_nominations': all_nominations})


@login_required
def nomi_apply(request, pk):
    nomination = Nomination.objects.get(pk=pk)
    ct = NominationInstance.objects.filter(nomination=nomination).filter(user=request.user).count()
    if not ct:
         ins = NominationInstance.objects.create(user=request.user, nomination=nomination)
         info = "Your application has been recorded"
         return render(request, 'nomi_done.html', context={'info': info})
    else:
        info = "You have applied for it already."

    return render(request, 'nomi_done.html', context={'info': info})


def result(request, pk):
    nomination = Nomination.objects.get(pk=pk)
    users = NominationInstance.objects.filter(nomination=nomination).filter(status__exact='a')

    return render(request, 'result.html', context={'users': users})


@permission_required('nomi.admin')
def application_result(request, pk):
    nomination = Nomination.objects.filter(pk=pk)
    applicants = NominationInstance.objects.filter(nomination=nomination)

    return render(request, 'applicants.html', context={'applicants': applicants})


@login_required
@permission_required('nomi.admin')
def accept_nomination(request, pk):
    application = NominationInstance.objects.get(pk=pk)
    id_accept = application.nomination.pk
    application.status = 'a'
    application.save()

    return HttpResponseRedirect(reverse('applicants', kwargs={'pk': id_accept}))


@login_required
@permission_required('nomi.admin')
def reject_nomination(request, pk):
    application = NominationInstance.objects.get(pk=pk)
    id_reject = application.nomination.pk
    application.status = 'r'
    application.save()

    return HttpResponseRedirect(reverse('applicants', kwargs={'pk': id_reject}))


class NominationCreate(CreateView):
    model = Nomination
    fields = ['name', 'description']
    success_url = reverse_lazy('index')


class NominationUpdate(UpdateView):
    model = Nomination
    fields = ['name', 'description']
    success_url = reverse_lazy('index')


class NominationDelete(DeleteView):
    model = Nomination
    success_url = reverse_lazy('index')


class UserProfileCreate(CreateView):
    model = UserProfile
    fields = '__all__'
    success_url = reverse_lazy('index')


class UserProfileUpdate(UpdateView):
    model = UserProfile
    fields = '__all__'
    success_url = reverse_lazy('index')































