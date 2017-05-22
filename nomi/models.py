from django.db import models
from django.contrib.auth.models import User


class Nomination(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name


class NominationInstance(models.Model):
    STATUS = (
        ('a', 'Accepted'),
        ('r', 'Rejected'),

    )

    nomination = models.ForeignKey('Nomination', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS,  null=True, blank=True, default=None)

    def __str__(self):
        return str(self.id)

