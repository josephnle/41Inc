# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-27 04:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='series',
            name='thumbnail_url',
        ),
        migrations.AddField(
            model_name='series',
            name='thumbnail',
            field=models.ImageField(default=None, upload_to='thumbnails'),
            preserve_default=False,
        ),
    ]
