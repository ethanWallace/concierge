# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-25 13:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default=None, null=True, upload_to='avatars/'),
        ),
    ]
