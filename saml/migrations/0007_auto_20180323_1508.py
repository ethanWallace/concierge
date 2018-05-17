# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-23 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saml', '0006_auto_20180323_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identityprovider',
            name='encryption_x509cert1',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='identityprovider',
            name='encryption_x509cert2',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='identityprovider',
            name='signing_x509cert2',
            field=models.TextField(blank=True),
        ),
    ]
