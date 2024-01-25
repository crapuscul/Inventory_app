# Generated by Django 5.0.1 on 2024-01-19 13:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0028_remove_supplier_invoice_payment_supplier_invoice_id_and_more'),
        ('srm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='supplier_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='srm.supplier'),
        ),
        migrations.DeleteModel(
            name='supplier',
        ),
    ]
