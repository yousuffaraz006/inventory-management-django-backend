# Generated by Django 5.1.2 on 2024-12-11 03:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0012_alter_purchase_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, max_length=25, null=True, unique=True)),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project_app.company')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]