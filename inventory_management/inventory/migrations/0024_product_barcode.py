# Generated by Django 5.0 on 2024-01-06 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0023_remove_product_barcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='barcode',
            field=models.ImageField(blank=True, null=True, upload_to='barcodes/'),
        ),
    ]
