# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-05 17:05
from __future__ import unicode_literals

from django.db import migrations, models
import nomi.models


class Migration(migrations.Migration):

    dependencies = [
        ('nomi', '0127_auto_20170805_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posthistory',
            name='end',
            field=models.DateField(blank=True, default=nomi.models.default_end_date),
        ),
        migrations.AlterField(
            model_name='posthistory',
            name='start',
            field=models.DateField(auto_now_add=True),
        ),
    ]
