from django.shortcuts import render
from .models import Nomination, NominationInstance, UserProfile
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from .forms import NominationForm
from forms.models import Questionnaire


def index(request):
    nominations = Nomination.objects.all()
    all_nominations = nominations[::-1]

    return render(request, 'index.html', context={'all_nominations': all_nominations})


@login_required
def nomi_apply(request, pk):
    nomination = Nomination.objects.get(pk=pk)
    ct = NominationInstance.objects.filter(nomination=nomination).filter(user=request.user).count()

    if not request.user.is_superuser:
        if not ct:
             ins = NominationInstance.objects.create(user=request.user, nomination=nomination)
             info = "Your application has been recorded"
             return render(request, 'nomi_done.html', context={'info': info})
        else:
            info = "You have applied for it already."

    else:
        info = "The nomination for your post has been created and is awaiting responses"
        return render(request, 'nomi_done.html', context={'info': info})

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


class NominationDelete(DeleteView):
    model = Nomination
    success_url = reverse_lazy('index')


@login_required
def profile_view(request):
    pk = request.user.pk

    try:
        user_profile = UserProfile.objects.get(user__id=pk)
        return render(request, 'profile.html', context={'user_profile': user_profile})
    except ObjectDoesNotExist:
        return HttpResponseRedirect('create')


class UserProfileCreate(CreateView):
    model = UserProfile
    fields = '__all__'
    success_url = reverse_lazy('index')


class UserProfileUpdate(UpdateView):
    model = UserProfile
    fields = '__all__'
    success_url = reverse_lazy('index')



def nomination_create(request):

    if request.method == 'POST':
        title_form = NominationForm(request.POST)
        if title_form.is_valid():

            questionnaire = Questionnaire.objects.create(name=title_form.cleaned_data['title'],
                                                         description=title_form.cleaned_data['description'])
            nomination=Nomination.objects.create(name=title_form.cleaned_data['title'],
                                                 description=title_form.cleaned_data['description'],
                                                 nomi_form=questionnaire)
            pk=questionnaire.pk
            return HttpResponseRedirect(reverse('forms:show_form', kwargs={'pk': pk}))

    else:
        title_form=NominationForm()


    return render(request, 'nomi/nomination_form.html', context={'form': title_form})



class NominationUpdate(UpdateView):
    model = Nomination
    fields = ['name', 'description']
    success_url = reverse_lazy('index')


