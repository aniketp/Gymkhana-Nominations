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


class ResultView(generic.ListView):
    template_name = 'result.html'
    context_object_name = 'all_nominations'

    def get_queryset(self):
        return NominationInstance.objects.filter(status__exact='a')


