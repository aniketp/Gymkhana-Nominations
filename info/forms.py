from django import forms
from nomi.models import Club,Post,Session
from datetime import date

def give_session(st_year):
    return str(st_year) + " - " + str(st_year+1)

def current_session():
    now = date.today()
    end = now.replace(day=31, month=3, year=now.year)

    if end > now:
        st_year = now.year - 1
    else:
        st_year = now.year

    session = Session.objects.filter(start_year=st_year).first()
    if session == None:
        session = Session.objects.create(start_year=st_year)

    return session


class ClubForm(forms.Form):
    club = forms.ChoiceField( choices=[('NA','------------')] + [(o.id, o) for o in Club.objects.all()],  widget=forms.Select,required= False )


class PostForm(forms.Form):
    def __init__(self, club, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if club:
            CHIOICE = [('','------------')] + [(o.id, o) for o in club.club_posts.all()]
            self.fields['post'] = forms.ChoiceField( choices= CHIOICE,widget=forms.Select,required= False)

        else:
            self.fields['post'] = forms.ChoiceField(choices=[(o.id, o) for o in Post.objects.all()], widget=forms.Select)



class SessionForm(forms.Form):
    CH = [(session.id, give_session(session.start_year)) for session in Session.objects.all()]
    CH = sorted(CH, key=lambda x: x[1])
    CH = CH[::-1]
    year = forms.ChoiceField( choices= CH,  widget=forms.Select , initial=current_session())
