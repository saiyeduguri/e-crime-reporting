# Generated by Django 4.2.7 on 2023-11-15 17:57

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ecr', '0005_alter_officer_managers'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('sensitive_data', django_cryptography.fields.encrypt(models.CharField(max_length=50))),
            ],
        ),
    ]
