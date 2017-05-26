# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-05-26 19:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FilledForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('questionnaire', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='forms.Questionnaire')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(choices=[('Short_answer', 'Short-answer'), ('Paragraph', 'long-answer'), ('Integer', 'Integer-answer'), ('ChoiceField', 'Choice'), ('MultipleChoiceField', 'Multiple-choice'), ('Date', 'date')], max_length=50, null=True)),
                ('question', models.CharField(max_length=300, null=True)),
                ('question_choices', models.TextField(blank=True, help_text='add dollar($) symbol between two choices', max_length=512, null=True)),
                ('questionnaire', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='forms.Questionnaire')),
            ],
        ),
        migrations.AddField(
            model_name='answerinstance',
            name='form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='forms.FilledForm'),
        ),
        migrations.AddField(
            model_name='answerinstance',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='forms.Question'),
        ),
    ]
