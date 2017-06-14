from django.contrib import admin
from .models import Questionnaire, Question, FilledForm


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Questionnaire, QuestionnaireAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('questionnaire', 'question_type', 'question', 'question_choices')

admin.site.register(Question, QuestionAdmin)


class FilledFormAdmin(admin.ModelAdmin):
    list_display = ('questionnaire', 'applicant')

admin.site.register(FilledForm, FilledFormAdmin)




