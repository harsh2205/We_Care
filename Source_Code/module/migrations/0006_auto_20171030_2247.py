# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-30 22:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0005_auto_20171030_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='startTime',
            field=models.TimeField(),
        ),
    ]
