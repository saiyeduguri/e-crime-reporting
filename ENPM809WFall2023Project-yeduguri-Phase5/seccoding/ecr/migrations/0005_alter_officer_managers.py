# Generated by Django 4.2.7 on 2023-11-15 00:06

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecr', '0004_alter_officer_username'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='officer',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
