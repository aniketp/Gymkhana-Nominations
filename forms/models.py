
from django.db import models
from django import forms
from django.contrib.auth.models import User


class Questionnaire(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=250, default=u"I'm a description!")
    status = models.CharField(max_length=100, null=True,blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

