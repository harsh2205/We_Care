# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-21 03:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0007_appointment_diagnostics'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment_Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=1000)),
            ],
        ),
    ]
