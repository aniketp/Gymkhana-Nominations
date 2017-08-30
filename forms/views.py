from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from .models import Questionnaire, Question, FilledForm
from .forms import BuildForm, BuildQuestion,DesForm
from django.views.generic.edit import UpdateView
import json




def creator_form(request, pk):
    questionnaire = get_object_or_404(Questionnaire, id=pk)
    nomi = questionnaire.nomination
    form = questionnaire.get_form(request.POST or None)
    pk = questionnaire.pk
    questions = Question.objects.filter(questionnaire=questionnaire)
    d_form = DesForm(request.POST or None, instance=nomi)
    if d_form.is_valid():
        d_form.save()
        return HttpResponseRedirect(reverse('forms:creator_form', kwargs={'pk': pk}))

    return render(request, 'forms/nomi_ques_and_des.html', context={'form': form, 'questions': questions, 'd_form': d_form,
                                                               'pk': pk,'nomi':nomi})


def add_ques(request, pk):
    questionnaire = Questionnaire.objects.get(pk=pk)
    nomi = questionnaire.nomination

    if request.method == 'POST':
        form = BuildQuestion(request.POST)
        if form.is_valid():
            Question.objects.create(questionnaire=questionnaire, question_type=form.cleaned_data['question_type'],
                                    question=form.cleaned_data['question'],
                                    question_choices=form.cleaned_data['question_choices'],required = form.cleaned_data['required'])

            return HttpResponseRedirect(reverse('forms:creator_form', kwargs={'pk': pk}))
    else:
        form = BuildQuestion()

    return render(request, 'forms/build_ques.html', context={'form': form, 'nomi':nomi})


class QuestionUpdate(UpdateView):
    model = Question
    fields = ['question', 'question_type', 'question_choices','required']
    template_name = 'forms/ques_update.html'

    def get_success_url(self):

        qk = self.kwargs['qk']
        return reverse('forms:creator_form', kwargs={'pk': qk})



def replicate(pk):
    questionnaire = Questionnaire.objects.get(pk=pk)
    new_questionnaire = Questionnaire.objects.create()
    for question in questionnaire.question_set.all():
        Question.objects.create(questionnaire=new_questionnaire, question_type=question.question_type,
                                question=question.question,
                                question_choices=question.question_choices)

    return new_questionnaire




