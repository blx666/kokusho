# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-17 03:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_auto_20170317_0309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]
