from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from .models import Questionnaire,Question,FilledForm,AnswerInstance,QUES_TYPES
from .forms import BuildForm,BuildQuestion

# Create your views here.
def index(request):
    forms=Questionnaire.objects.all()
    return render(request, 'forms/index.html',context={'forms':forms})

def show_form(request,pk):
    questionnaire = get_object_or_404(Questionnaire, id=pk)
    form = questionnaire.get_form(request.POST or None)
    pk=questionnaire.pk
    if form.is_valid():
        questionnaire.add_answer(request.user, form.cleaned_data)

    return render(request, 'forms/d_forms.html', context={'form': form,'questionnaire':questionnaire,'pk':pk})


def build_form(request):
    if request.method == 'POST':
        form = BuildForm(request.POST)
        if form.is_valid():
            ques=Questionnaire.objects.create(name=form.cleaned_data['title'], description=form.cleaned_data['description'])
            pk=ques.id
            return HttpResponseRedirect(reverse('show_form',kwargs={'pk': pk}))
    else:
        form = BuildForm()

    return render(request, 'forms/build_form.html',context={'form':form})

def add_ques(request,pk):
    questionnaire=Questionnaire.objects.get(pk=pk)

    if request.method == 'POST':
        form = BuildQuestion(request.POST)
        if form.is_valid():
            Question.objects.create(questionnaire=questionnaire,question_type=form.cleaned_data['question_type'],question=form.cleaned_data['question'],question_choices=form.cleaned_data['question_choices'])

            return HttpResponseRedirect(reverse('show_form',kwargs={'pk': pk}))
    else:
        form = BuildQuestion()

    return render(request, 'forms/build_ques.html',context={'form':form,'questionnaire':questionnaire})

