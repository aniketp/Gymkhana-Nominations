# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-05 10:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nomi', '0114_auto_20170805_0844'),
    ]

    operations = [
        migrations.AddField(
            model_name='nomination',
            name='re_opening_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='status',
            field=models.CharField(choices=[('Nomination created', 'Nomination created'), ('Nomination out', 'Nomination out'), ('Interview period', 'Interview period'), ('Interview period and Reopening initiated', 'Interview period and Reopening initiated'), ('Interview period and Nomination reopened', 'Interview period and Nomination reopened'), ('Sent for ratification', 'Sent for ratification'), ('Work done', 'Work done')], default='Nomination created', max_length=50),
        ),
        migrations.AlterField(
            model_name='reopennomination',
            name='nomi',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='nomi.Nomination'),
        ),
    ]
