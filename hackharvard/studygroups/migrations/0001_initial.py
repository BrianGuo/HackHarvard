# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-23 00:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=30)),
                ('number', models.CharField(max_length=4)),
                ('title', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='DateDuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(choices=[('M', 'Monday'), ('T', 'Tuesday'), ('W', 'Wednesday'), ('R', 'Thursday'), ('F', 'Friday'), ('S', 'Saturday'), ('U', 'Sunday')], max_length=1)),
                ('time_start', models.TimeField()),
                ('time_end', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=50)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studygroups.Course')),
                ('meeting_time', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='studygroups.DateDuration')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('resume_or_linkedin', models.URLField()),
                ('bio', models.TextField()),
                ('courses', models.ManyToManyField(to='studygroups.Course')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(to='studygroups.Profile'),
        ),
        migrations.AddField(
            model_name='dateduration',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studygroups.Profile'),
        ),
    ]
