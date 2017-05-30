from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse,reverse_lazy
from .models import Questionnaire, Question,FilledForm,QUES_TYPES
from .forms import BuildForm, BuildQuestion
import json
from django.views.generic.edit import CreateView, UpdateView, DeleteView


def index(request):
    forms = Questionnaire.objects.all()
    return render(request, 'forms/index.html', context={'forms': forms})


def creator_form(request, pk):
    questionnaire = get_object_or_404(Questionnaire, id=pk)
    form = questionnaire.get_form(request.POST or None)
    pk = questionnaire.pk
    questions=Question.objects.filter(questionnaire=questionnaire)

    return render(request, 'forms/creator_form.html', context={'form': form,'questions':questions, 'questionnaire':questionnaire,'pk':pk})


def show_form(request, pk):
    questionnaire = get_object_or_404(Questionnaire, id=pk)
    form = questionnaire.get_form(request.POST or None)
    pk = questionnaire.pk
    tk=questionnaire.nomination.pk
    if form.is_valid():
        questionnaire.add_answer(request.user, form.cleaned_data)
        return HttpResponseRedirect(reverse('nomi_apply',kwargs={'pk':tk}))

    return render(request, 'forms/d_forms.html', context={'form': form, 'questionnaire':questionnaire,'pk':pk})











def show_answer_form(request,pk):
    questionnaire = get_object_or_404(Questionnaire, id=pk)
    filled_form = FilledForm.objects.filter(questionnaire=questionnaire).filter(applicant=request.user)
    actual_form = filled_form[0]
    data = json.loads(actual_form.data)
    form = questionnaire.get_form(data)
    return render(request, 'forms/ans_form.html', context={'form': form})




def build_form(request):
    if request.method == 'POST':
        form = BuildForm(request.POST)
        if form.is_valid():
            ques = Questionnaire.objects.create(name=form.cleaned_data['title'], description=form.cleaned_data['description'])
            pk = ques.id
            return HttpResponseRedirect(reverse('forms:show_form', kwargs={'pk': pk}))
    else:
        form = BuildForm()

    return render(request, 'forms/build_form.html', context={'form': form})


def add_ques(request, pk):
    questionnaire = Questionnaire.objects.get(pk=pk)

    if request.method == 'POST':
        form = BuildQuestion(request.POST)
        if form.is_valid():
            Question.objects.create(questionnaire=questionnaire, question_type=form.cleaned_data['question_type'], question=form.cleaned_data['question'], question_choices=form.cleaned_data['question_choices'])

            return HttpResponseRedirect(reverse('forms:show_form', kwargs={'pk': pk}))
    else:
        form = BuildQuestion()

    return render(request, 'forms/build_ques.html', context={'form': form, 'questionnaire': questionnaire})

class QuestionUpdate(UpdateView):
    model = Question
    fields = ['question','question_type','question_choices']
    template_name='forms/ques_update.html'

    def get_success_url(self):

        qk = self.kwargs['qk']
        return reverse('forms:creator_form', kwargs={'pk': qk})

