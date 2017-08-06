# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-05 09:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nomi', '0113_auto_20170712_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='commment',
            name='name_length',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nominationinstance',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]