from django.contrib import admin
from .models import Questionnaire,Question,FilledForm,AnswerInstance

admin.site.register(Questionnaire)
admin.site.register(Question)
admin.site.register(FilledForm)
admin.site.register(AnswerInstance)

