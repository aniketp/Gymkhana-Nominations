# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomi', '0144_auto_20170811_1728'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='year',
        ),
    ]
