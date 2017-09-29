from django import forms
from .models import QUES_TYPES,Question
from nomi.models import Nomination


# in use
class BuildQuestion(forms.Form):

    question_type = forms.CharField(max_length=50,widget=forms.Select(choices=QUES_TYPES))
    question = forms.CharField(max_length=400)
    question_choices = forms.CharField(max_length=512,widget=forms.Textarea,label_suffix=' *',
                                       help_text='add choices in separate lines', required=False)
    required = forms.BooleanField(initial=True,required = False)


class BuildForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()


class QuesForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_type','question','question_choices','required')

class DesForm(forms.ModelForm):
    class Meta:
        model = Nomination
        labels = {
            "name": "Title"}

        fields = ('name','description','deadline')