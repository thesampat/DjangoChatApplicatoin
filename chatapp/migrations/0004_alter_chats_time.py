# Generated by Django 4.1.1 on 2022-10-03 12:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0003_rename_chats_chats_chat_remove_chats_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chats',
            name='time',
            field=models.TimeField(verbose_name=datetime.datetime(2022, 10, 3, 18, 6, 23, 434132)),
        ),
    ]
