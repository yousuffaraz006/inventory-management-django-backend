# Generated by Django 5.1.2 on 2024-12-12 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0015_alter_employee_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]