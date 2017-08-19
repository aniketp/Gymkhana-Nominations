from django.db import models
from django.contrib.auth.models import User
from .choices import *
from datetime import datetime,date
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

def default_end_date():
    now = datetime.now()
    end = now.replace(day=31, month=3, year=now.year)

    if end > now:
        return end
    else:
        next_year = now.year + 1
        return end.replace(year=next_year)

def session_end_date(session):
    now = date.today()
    next_year = session + 1
    return now.replace(day=31, month=3, year=next_year)

class Session(models.Model):
    start_year = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.start_year)

class Club(models.Model):
    club_name = models.CharField(max_length=100, null=True)
    club_parent = models.ForeignKey('self', null=True, blank=True)


    def __str__(self):
        return self.club_name


class ClubCreate(models.Model):
    club_name = models.CharField(max_length=100, null=True)
    club_parent = models.ForeignKey('self', null=True, blank=True)
    take_approval = models.ForeignKey('Post', related_name="give_club_approval", on_delete=models.SET_NULL, null=True,blank=True)
    requested_by = models.ForeignKey('Post', related_name="club_request", on_delete=models.SET_NULL, null=True,blank=True)
    def __str__(self):
        return self.club_name


class Post(models.Model):
    post_name = models.CharField(max_length=500, null=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Club, related_name='club_posts', symmetrical=False, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    elder_brother = models.ForeignKey('self', related_name="little_bro", on_delete=models.CASCADE, null=True,blank=True)
    post_holders = models.ManyToManyField(User, related_name='posts', blank=True)
    post_approvals = models.ManyToManyField('self', related_name='approvals', symmetrical=False, blank=True)
    take_approval = models.ForeignKey('self', related_name="give_approval", on_delete=models.SET_NULL, null=True,blank=True)
    status = models.CharField(max_length=50, choices=POST_STATUS, default='Post created')
    perms = models.CharField(max_length=200, choices=POST_PERMS, default='normal')

    def __str__(self):
        return self.post_name

    def remove_holders(self):
        for holder in self.post_holders.all():
            history = PostHistory.objects.get(post=self, user=holder)

            if datetime.now() > history.end:
                self.post_holders.remove(holder)

        return self.post_holders


class PostHistory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    start = models.DateField(auto_now_add=True)
    end = models.DateField(null=True, blank=True, editable=True)
    post_session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)


class Nomination(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=20000, null=True, blank=True)
    brief_desc = models.TextField(max_length=300, null=True, blank=True)
    nomi_post = models.ForeignKey(Post, null=True)
    nomi_form = models.OneToOneField('forms.Questionnaire', null=True, blank=True)
    nomi_session = models.IntegerField(null=True)

    status = models.CharField(max_length=50, choices=STATUS, default='Nomination created')
    result_approvals = models.ManyToManyField(Post, related_name='result_approvals', symmetrical=False, blank=True)
    nomi_approvals = models.ManyToManyField(Post, related_name='nomi_approvals', symmetrical=False, blank=True)

    group_status = models.CharField(max_length=50, choices=GROUP_STATUS, default='normal')

    tags = models.ManyToManyField(Club, related_name='club_nomi', symmetrical=False, blank=True)

    opening_date = models.DateField(null=True, blank=True)
    re_opening_date = models.DateField(null=True, blank=True, editable=True)
    deadline = models.DateField(null=True, blank=True, editable=True)



    interview_panel = models.ManyToManyField(User, related_name='panel', symmetrical=False, blank=True)

    year_choice = models.CharField(max_length=100, choices=YEAR_1, null=True)
    hall_choice = models.CharField(max_length=100, choices=HALL_1, null=True)
    dept_choice = models.CharField(max_length=100, choices=DEPT_1, null=True)

    def __str__(self):
        return self.name

    def append(self):
        selected = NominationInstance.objects.filter(nomination=self, status='Accepted')
        st_year = self.nomi_session


        session = Session.objects.filter(start_year=st_year).first()
        if session is None:
            session = Session.objects.create(start_year = st_year)

        self.status = 'Work done'
        self.save()
        for each in selected:
            PostHistory.objects.create(post=self.nomi_post, user=each.user, end=session_end_date(session.start_year),
                                       post_session = session)
            self.nomi_post.post_holders.add(each.user)

        return self.nomi_post.post_holders

    def replace(self):
        for holder in self.nomi_post.post_holders.all():
            history = PostHistory.objects.get(post=self.nomi_post, user=holder)
            history.end = default_end_date()
            history.save()

        self.nomi_post.post_holders.clear()

        self.append()
        return self.nomi_post.post_holders

    def open_to_users(self):
        self.status = 'Nomination out'
        self.opening_date = datetime.now()
        self.save()
        return self.status


class ReopenNomination(models.Model):
    nomi = models.OneToOneField(Nomination, on_delete=models.CASCADE)
    approvals = models.ManyToManyField(Post,symmetrical=False)
    reopening_date = models.DateField(null=True, blank=True)

    def re_open_to_users(self):
        self.nomi.status = 'Interview period and Nomination reopened'
        self.nomi.re_opening_date = datetime.now()
        self.nomi.save()
        return self.nomi


class GroupNomination(models.Model):
    name = models.CharField(max_length=2000, null=True)
    description = models.CharField(max_length=5000, null=True, blank=True)
    nominations = models.ManyToManyField(Nomination, symmetrical=False, blank=True)
    status = models.CharField(max_length=50, choices=G_STATUS, default='created')
    opening_date = models.DateField(null=True, blank=True, default=timezone.now)
    approvals = models.ManyToManyField(Post, related_name='group_approvals', symmetrical=False, blank=True)
    tags = models.ManyToManyField(Club, related_name='club_group', symmetrical=False, blank=True)

    def __str__(self):
        return str(self.name)


class NominationInstance(models.Model):
    nomination = models.ForeignKey('Nomination', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=NOMI_STATUS,  null=True, blank=True, default=None)
    interview_status = models.CharField(max_length=20, choices=INTERVIEW_STATUS,  null=True, blank=True,
                                        default='Interview Not Done')
    filled_form = models.OneToOneField('forms.FilledForm', null=True, blank=True)
    timestamp = models.DateField(auto_now_add=True)
    edit_time = models.DateField(null=True, default=datetime.now())

    def __str__(self):
        return str(self.user) + ' ' + str(self.id)


class Deratification(models.Model):
    name = models.ForeignKey(User, max_length=30, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=DERATIFICATION, default='safe')
    deratify_approval = models.ForeignKey(Post, related_name='to_deratify',on_delete=models.CASCADE,null = True)


class Commment(models.Model):
    comments = models.TextField(max_length=1000, null=True, blank=True)
    nomi_instance = models.ForeignKey(NominationInstance, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_img = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    name = models.CharField(max_length=40, blank=True)
    roll_no = models.IntegerField(null=True)
    programme = models.CharField(max_length=7, choices=PROGRAMME, default='B.Tech')
    department = models.CharField(max_length=200, choices=DEPT, default='AE')
    hall = models.CharField(max_length=10, choices=HALL, default=1)
    room_no = models.CharField(max_length=10, null=True, blank=True)
    contact = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def image_url(self):
        if self.user_img and hasattr(self.user_img, 'url'):
            return self.user_img.url
        else:
            return '/static/nomi/img/banner.png'


@receiver(post_save, sender=Nomination)
def ensure_parent_in_approvals(sender, **kwargs):
    nomi = kwargs.get('instance')
    post = nomi.nomi_post
    if post:
        parent = post.parent
        nomi.nomi_approvals.add(parent)
        nomi.result_approvals.add(parent)
        nomi.tags.add(post.club)
        nomi.tags.add(parent.club)


    if nomi.description:
        if not nomi.brief_desc:
            nomi.brief_desc = nomi.description[:280]
            nomi.save()


@receiver(post_save, sender=Post)
def ensure_parent_in_post_approvals(sender, **kwargs):
    post = kwargs.get('instance')
    if post:
        parent = post.parent
        if parent:
            post.post_approvals.add(parent)
            post.tags.add(parent.club)

        big_bro = post.elder_brother
        if big_bro:
            post.tags.add(big_bro.club)

        if post.club:
            post.tags.add(post.club)


