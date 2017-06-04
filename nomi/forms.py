from django import forms


class NominationForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)


class PostForm(forms.Form):
    # club_name = forms.CharField()
    post_title = forms.CharField()





