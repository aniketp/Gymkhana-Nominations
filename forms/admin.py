from django.contrib import admin
from .models import Questionnaire, Question, FilledForm, AnswerInstance


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'status')

admin.site.register(Questionnaire, QuestionnaireAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('questionnaire', 'question_type', 'question', 'question_choices')

admin.site.register(Question, QuestionAdmin)


class FilledFormAdmin(admin.ModelAdmin):
    list_display = ('questionnaire', 'applicant')

admin.site.register(FilledForm, FilledFormAdmin)


class AnswerInstanceAdmin(admin.ModelAdmin):
    list_display = ('form', 'question', 'answer',)

admin.site.register(AnswerInstance, AnswerInstanceAdmin)

