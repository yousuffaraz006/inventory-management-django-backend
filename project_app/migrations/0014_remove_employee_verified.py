# Generated by Django 5.1.2 on 2024-12-11 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0013_employee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='verified',
        ),
    ]
