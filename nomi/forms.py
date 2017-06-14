from django import forms
from .choices import *
from .models import NominationInstance

class NominationForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    year_choice = forms.ChoiceField(choices=YEAR_1, label="Batch", initial='All', widget=forms.Select(), required=True)
    dept_choice = forms.ChoiceField(choices=DEPT_1, label="Dept", initial='All', widget=forms.Select(), required=True)
    hall_choice = forms.ChoiceField(choices=HALL_1, label="Hall", initial=0, widget=forms.Select(), required=True)


class PostForm(forms.Form):
    # club_name = forms.CharField()
    post_title = forms.CharField()


class ClubForm(forms.Form):
    club_name = forms.CharField()


class ConfirmApplication(forms.Form):
    Tick_the_box_for_confirmation = forms.CharField(max_length=100, widget=forms.CheckboxInput())


class CommentForm(forms.ModelForm):
    class Meta:
        model = NominationInstance
        fields=['comments']


class UserId(forms.Form):
    user_roll = forms.IntegerField()