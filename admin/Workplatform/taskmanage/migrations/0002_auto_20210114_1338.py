# Generated by Django 2.2.5 on 2021-01-14 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='end_time',
            field=models.DateTimeField(max_length=20, null=True, verbose_name='任务结束时间'),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_time',
            field=models.DateTimeField(max_length=20, verbose_name='任务开始时间'),
        ),
    ]
