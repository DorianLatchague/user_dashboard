# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-11-09 22:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User_interface', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='description',
            new_name='desc',
        ),
    ]
