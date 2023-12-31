# Generated by Django 5.0 on 2023-12-30 14:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="subfamily_id",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="inventory.sub_family",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="supplier_id",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="inventory.supplier",
            ),
        ),
    ]
