# Generated by Django 5.1.2 on 2024-12-13 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0018_rename_company_companie'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companie',
            old_name='address',
            new_name='company_address',
        ),
        migrations.RenameField(
            model_name='companie',
            old_name='email',
            new_name='company_email',
        ),
        migrations.RenameField(
            model_name='companie',
            old_name='name',
            new_name='company_name',
        ),
        migrations.RenameField(
            model_name='companie',
            old_name='user',
            new_name='founder',
        ),
        migrations.RenameField(
            model_name='companymember',
            old_name='user',
            new_name='member',
        ),
        migrations.RenameField(
            model_name='companymember',
            old_name='email',
            new_name='member_email',
        ),
        migrations.RenameField(
            model_name='companymember',
            old_name='name',
            new_name='member_name',
        ),
        migrations.RenameField(
            model_name='companymember',
            old_name='phone',
            new_name='member_phone',
        ),
        migrations.RenameField(
            model_name='companymember',
            old_name='verified',
            new_name='member_verified',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='name',
            new_name='product_name',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='rate',
            new_name='product_rate',
        ),
        migrations.RenameField(
            model_name='purchase',
            old_name='date',
            new_name='purchase_date',
        ),
        migrations.RenameField(
            model_name='purchase',
            old_name='slug',
            new_name='purchase_slug',
        ),
        migrations.RenameField(
            model_name='purchase',
            old_name='total',
            new_name='purchase_total',
        ),
        migrations.RenameField(
            model_name='purchaseitem',
            old_name='cost',
            new_name='p_item_cost',
        ),
        migrations.RenameField(
            model_name='purchaseitem',
            old_name='product',
            new_name='p_item_product',
        ),
        migrations.RenameField(
            model_name='purchaseitem',
            old_name='quantity',
            new_name='p_item_quantity',
        ),
        migrations.AddField(
            model_name='companymember',
            name='member_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]