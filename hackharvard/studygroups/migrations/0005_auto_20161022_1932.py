# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-22 19:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studygroups', '0004_auto_20161022_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='../static/images'),
        ),
    ]