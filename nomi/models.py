from django.db import models
from django.contrib.auth.models import User
from .choices import *


class Club(models.Model):
    club_name = models.CharField(max_length=100, null=True)
    club_parent = models.ForeignKey('self', null=True, blank=True)
    club_members = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.club_name


class Post(models.Model):
    post_name = models.CharField(max_length=500, null=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    post_holders = models.ManyToManyField(User, blank=True)
    post_approvals = models.ManyToManyField('self', related_name='approvals', symmetrical=False, blank=True)
    status = models.CharField(max_length=50, choices=POST_STATUS, default='Post created')

    def __str__(self):
        return self.post_name


class Nomination(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, null=True, blank=True)
    results_declared = models.BooleanField(default=False)
    nomi_post = models.ForeignKey(Post, null=True)
    nomi_form = models.OneToOneField('forms.Questionnaire', null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS, default='Nomination created')

    year_choice = models.CharField(max_length=100, choices=YEAR_1, null=True)
    hall_choice = models.CharField(max_length=100, choices=HALL_1, null=True)
    dept_choice = models.CharField(max_length=100, choices=DEPT_1, null=True)

    def __str__(self):
        return self.name


class NominationInstance(models.Model):
    nomination = models.ForeignKey('Nomination', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=1, choices=NOMI_STATUS,  null=True, blank=True, default=None)
    filled_form = models.OneToOneField('forms.FilledForm', null=True)

    def __str__(self):
        return str(self.user) + ' ' + str(self.id)


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, blank=True)
    roll_no = models.IntegerField(null=True)
    year = models.CharField(max_length=4, choices=YEAR, default='Y16')
    programme = models.CharField(max_length=7, choices=PROGRAMME, default='B.Tech')
    department = models.CharField(max_length=200, choices=DEPT, default=None)
    hall = models.CharField(max_length=10, choices=HALL, default=1)
    room_no = models.CharField(max_length=10, null=True)

    def __str__(self):
        return str(self.name)


