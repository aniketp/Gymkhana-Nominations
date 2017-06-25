from django import forms
from nomi.models import Club,Post


class ClubForm(forms.Form):
    club = forms.ChoiceField( choices=[('','------------')] + [(o.id, o) for o in Club.objects.all()],  widget=forms.Select )


class PostForm(forms.Form):
    def __init__(self, club, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if club:
            CHIOICE = [('','------------')] + [(o.id, o) for o in club.club_posts.all()]
            self.fields['post'] = forms.ChoiceField( choices= CHIOICE,widget=forms.Select,required= False)

        else:
            self.fields['post'] = forms.ChoiceField(choices=[(o.id, o) for o in Post.objects.all()], widget=forms.Select)