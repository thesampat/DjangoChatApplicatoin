# Generated by Django 4.1.1 on 2022-10-06 04:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0016_alter_chats_time_alter_redisuser_active_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chats',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 6, 10, 12, 17, 814724)),
        ),
        migrations.AlterField(
            model_name='redisuser',
            name='active_status',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]