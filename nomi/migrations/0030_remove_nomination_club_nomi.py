# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 09:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomi', '0029_club_club_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nomination',
            name='club_nomi',
        ),
    ]
