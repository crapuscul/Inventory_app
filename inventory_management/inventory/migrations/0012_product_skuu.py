# Generated by Django 5.0 on 2024-01-05 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_remove_product_skuu'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='skuu',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]