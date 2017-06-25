from django.db import models
from django.contrib.auth.models import User
from .choices import *
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone


class Club(models.Model):
    club_name = models.CharField(max_length=100, null=True)
    club_parent = models.ForeignKey('self', null=True, blank=True)

    def __str__(self):
        return self.club_name


class Post(models.Model):
    post_name = models.CharField(max_length=500, null=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Club, related_name='club_posts', symmetrical=False,blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    post_holders = models.ManyToManyField(User, related_name='posts', blank=True)
    post_approvals = models.ManyToManyField('self', related_name='approvals', symmetrical=False, blank=True)
    status = models.CharField(max_length=50, choices=POST_STATUS, default='Post created')
    perms = models.CharField(max_length=200, choices=POST_PERMS, default='normal')
    tag_perms = models.CharField(max_length=20, choices=TAG_PERMS, default='normal')

    def __str__(self):
        return self.post_name

    def remove_holders(self):
        for holder in self.post_holders.all():
            history = PostHistory.objects.get(post=self, user=holder)
            history.end = datetime.now()
            history.save()

        self.post_holders.clear()
        return self.post_holders


class PostHistory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    start = models.DateField(auto_now_add=True)
    end = models.DateField(null=True, blank=True, editable=True)


class Nomination(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=20000, null=True, blank=True)
    brief_desc = models.TextField(max_length=300, null=True, blank=True)
    nomi_post = models.ForeignKey(Post, null=True)
    nomi_form = models.OneToOneField('forms.Questionnaire', null=True, blank=True)

    status = models.CharField(max_length=50, choices=STATUS, default='Nomination created')
    result_approvals = models.ManyToManyField(Post, related_name='result_approvals', symmetrical=False, blank=True)
    nomi_approvals = models.ManyToManyField(Post, related_name='nomi_approvals', symmetrical=False, blank=True)
    group_status = models.CharField(max_length=50, choices= GROUP_STATUS, default='normal')
    tags = models.ManyToManyField(Club, related_name='club_nomi', symmetrical=False, blank=True)

    opening_date = models.DateField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True, editable=True)

    year_choice = models.CharField(max_length=100, choices=YEAR_1, null=True)
    hall_choice = models.CharField(max_length=100, choices=HALL_1, null=True)
    dept_choice = models.CharField(max_length=100, choices=DEPT_1, null=True)

    def __str__(self):
        return self.name

    def append(self):
        selected = NominationInstance.objects.filter(nomination=self, status='Accepted')
        self.status = 'Work done'
        self.save()
        for each in selected:
            PostHistory.objects.create(post=self.nomi_post, user=each.user)
            self.nomi_post.post_holders.add(each.user)

        return self.nomi_post.post_holders

    def replace(self):
        for holder in self.nomi_post.post_holders.all():
            history = PostHistory.objects.get(post=self.nomi_post, user=holder)
            history.end = datetime.now()
            history.save()

        self.nomi_post.post_holders.clear()
        self.append()
        return self.nomi_post.post_holders

    def open_to_users(self):
        self.status = 'Nomination out'
        self.opening_date = datetime.now()
        self.save()
        return self.status


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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=NOMI_STATUS,  null=True, blank=True, default=None)
    interview_status = models.CharField(max_length=20, choices=INTERVIEW_STATUS,  null=True, blank=True,
                                        default='Interview Not Done')
    filled_form = models.OneToOneField('forms.FilledForm', null=True, blank=True)

    def __str__(self):
        return str(self.user) + ' ' + str(self.id)


class Commment(models.Model):
    comments = models.TextField(max_length=1000, null=True, blank=True)
    nomi_instance = models.ForeignKey(NominationInstance, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_img = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    name = models.CharField(max_length=40, blank=True)
    roll_no = models.IntegerField(null=True)
    year = models.CharField(max_length=4, choices=YEAR, default='Y16')
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
        nomi.result_approvals.add(post)
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

        if post.club:
            post.tags.add(post.club)
        

