# Generated by Django 5.0 on 2024-01-03 10:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_rename_sub_family_subfamily'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='family_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.family'),
        ),
    ]
