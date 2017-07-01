from django import forms
from .models import QUES_TYPES
from nomi.models import Nomination


# in use
class BuildQuestion(forms.Form):

    question_type = forms.CharField(max_length=50,widget=forms.Select(choices=QUES_TYPES))
    question = forms.CharField(max_length=300)
    question_choices = forms.CharField(max_length=512,widget=forms.Textarea,
                                       help_text='add choices in separate lines', required=False)

# no use as of now
class BuildForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()



class DesForm(forms.ModelForm):
    class Meta:
        model = Nomination
        fields = ('description',)