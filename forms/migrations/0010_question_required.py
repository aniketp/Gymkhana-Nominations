# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-30 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0009_auto_20170819_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='required',
            field=models.BooleanField(default=True),
        ),
    ]
