from django import forms
from .choices import *
from .models import *


class NominationForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    year_choice = forms.ChoiceField(choices=YEAR_1, label="Batch", initial='All', widget=forms.Select(), required=True)
    dept_choice = forms.ChoiceField(choices=DEPT_1, label="Dept", initial='All', widget=forms.Select(), required=True)
    hall_choice = forms.ChoiceField(choices=HALL_1, label="Hall", initial=0, widget=forms.Select(), required=True)


class PostForm(forms.Form):
    def __init__(self, parent, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['post_name'] = forms.CharField()
        if parent.club.club_set.all():
            self.fields['club'] = forms.ChoiceField(
                choices=[(o.id, o) for o in Club.objects.filter(club_parent=parent.club)],
                widget=forms.Select
         )
        else:
            self.fields['club'] = forms.ChoiceField(
                choices=[(parent.club.id, parent.club)],
                widget=forms.Select)


class ClubForm(forms.Form):
    club_name = forms.CharField()


class ConfirmApplication(forms.Form):
    Tick_the_box_for_confirmation = forms.CharField(max_length=100, widget=forms.CheckboxInput())


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)


class UserId(forms.Form):
    user_roll = forms.IntegerField()


class SelectNomiForm(forms.Form):
    def __init__(self, post, *args, **kwargs):
        super(SelectNomiForm, self).__init__(*args, **kwargs)
        self.fields['group'] = forms.MultipleChoiceField(
            choices=[(o.id, o) for o in Nomination.objects.filter(nomi_approvals=post).filter(status='Nomination created')],
            widget=forms.CheckboxSelectMultiple
        )


class GroupNominationForm(forms.Form):
    title = forms.CharField()
