# Generated by Django 4.1.1 on 2022-10-05 04:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0011_remove_redisuser_last_seeen_redisuser_last_seen_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chats',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 5, 9, 32, 49, 202311)),
        ),
        migrations.AlterField(
            model_name='redisuser',
            name='last_seen',
            field=models.DateTimeField(default='none'),
        ),
    ]
