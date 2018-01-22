# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-05 14:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0024_auto_20171205_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='cost',
            field=models.CharField(default=0, max_length=1000),
        ),
        migrations.AlterField(
            model_name='batch',
            name='count',
            field=models.CharField(default=0, max_length=1000),
        ),
        migrations.AlterField(
            model_name='batch',
            name='power',
            field=models.CharField(default=0, max_length=1000),
        ),
        migrations.AlterField(
            model_name='bills',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='module.Bill_status'),
        ),
        migrations.AlterField(
            model_name='prescription_details',
            name='prescription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='module.Prescription_List'),
        ),
    ]
