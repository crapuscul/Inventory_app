# Generated by Django 5.0 on 2024-01-03 11:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_product_family_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='family_id',
        ),
        migrations.AlterField(
            model_name='product',
            name='subfamily',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.subfamily'),
        ),
    ]