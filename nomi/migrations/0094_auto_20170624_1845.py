# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-24 18:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nomi', '0093_userprofile_user_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='club',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='post',
        ),
        migrations.AlterField(
            model_name='commment',
            name='comments',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]