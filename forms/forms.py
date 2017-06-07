from django import forms
from .models import QUES_TYPES


# in use
class BuildQuestion(forms.Form):

    question_type = forms.CharField(max_length=50,widget=forms.Select(choices=QUES_TYPES))
    question = forms.CharField(max_length=300)

# no use as of now
class BuildForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()

question_choices = forms.CharField(max_length=512,widget=forms.Textarea, help_text='add dollar($) symbol between two choices',required=False)