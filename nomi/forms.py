from django import forms
from .choices import *


class NominationForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    year = forms.ChoiceField(choices=YEAR_1, label="Batch", initial='All', widget=forms.Select(), required=True)
    department = forms.ChoiceField(choices=DEPT_1, label="Dept", initial='All', widget=forms.Select(), required=True)
    hall = forms.ChoiceField(choices=HALL_1, label="Hall", initial=0, widget=forms.Select(), required=True)


class PostForm(forms.Form):
    # club_name = forms.CharField()
    post_title = forms.CharField()





