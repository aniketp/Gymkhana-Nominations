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
    if session is None:
        session = Session.objects.create(start_year=st_year)

    return session


def make_club_choice(parent,i):
    global GLOBAL_CHOICE
    child_clubs = Club.objects.filter(club_parent = parent)

    if parent is None:
        GLOBAL_CHOICE = [('NA', 'ALL')]
    else:
        if parent.club_parent is None:
            pass
        else:
            GLOBAL_CHOICE = GLOBAL_CHOICE + [(parent.id , '. ' *2*  i + '' + ' ' + str(parent))]


    if child_clubs:
        for each in child_clubs:
            make_club_choice(each,i+1)

    return GLOBAL_CHOICE





class ClubForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ClubForm, self).__init__(*args, **kwargs)
        self.fields["club"] = forms.ChoiceField( choices=make_club_choice(None,-2),  widget=forms.Select,required= False )


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
