# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-01 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websites', '0007_auto_20160601_0727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='main_bg_color',
            field=models.CharField(default='#666', max_length=10),
        ),
        migrations.AlterField(
            model_name='info',
            name='main_color',
            field=models.CharField(default='#fff', max_length=10),
        ),
    ]
