# Generated by Django 5.1.2 on 2024-12-02 13:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0007_alter_product_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('total', models.FloatField(blank=True, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project_app.company')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.IntegerField(blank=True, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project_app.product')),
                ('purchase', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project_app.purchase')),
            ],
        ),
    ]