# Generated by Django 5.0 on 2024-01-05 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0021_remove_product_sku'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sku',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]