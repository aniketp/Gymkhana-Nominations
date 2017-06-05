from django import forms
from .models import UserProfile


class NominationForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    hall = forms.ChoiceField(choices=UserProfile.HALL, label="Hall", initial='', required=True)


class PostForm(forms.Form):
    # club_name = forms.CharField()
    post_title = forms.CharField()





