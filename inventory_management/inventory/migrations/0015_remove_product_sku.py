# Generated by Django 5.0 on 2024-01-05 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_product_sku'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sku',
        ),
    ]
