# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2021-01-07 02:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210106_1352'),
        ('taskmanage', '0007_auto_20210106_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.UserInfo', verbose_name='创建人'),
            preserve_default=False,
        ),
    ]
