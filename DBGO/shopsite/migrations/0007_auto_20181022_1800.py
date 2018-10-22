# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-22 10:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopsite', '0006_normaluser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='normaluser',
            name='header',
            field=models.ImageField(default='static/images/headers/default.jpg', upload_to='static/images/headers', verbose_name='用户头像'),
        ),
    ]
