# Generated by Django 4.1.1 on 2022-10-06 04:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0014_alter_chats_time_alter_redisuser_last_seen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='redisuser',
            name='last_seen',
        ),
        migrations.AddField(
            model_name='redisuser',
            name='active_status',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 6, 10, 6, 22, 499219), null=True),
        ),
        migrations.AlterField(
            model_name='chats',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 6, 10, 6, 22, 499519)),
        ),
    ]
