# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-05 12:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0022_auto_20171205_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription_details',
            name='batch',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='module.Batch'),
            preserve_default=False,
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