# Generated by Django 5.1.2 on 2024-12-01 15:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0004_alter_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project_app.company'),
        ),
    ]
