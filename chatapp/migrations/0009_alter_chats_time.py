# Generated by Django 4.1.1 on 2022-10-04 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0008_alter_chats_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chats',
            name='time',
            field=models.DateTimeField(default='18:52'),
        ),
    ]