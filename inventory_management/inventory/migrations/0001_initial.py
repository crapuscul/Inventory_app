# Generated by Django 5.0 on 2023-12-28 21:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="customer",
            fields=[
                ("customer_id", models.IntegerField(primary_key=True, serialize=False)),
                ("customer_name", models.CharField(max_length=255)),
                ("customer_city", models.CharField(max_length=255)),
                ("customer_phone", models.CharField(max_length=20)),
                ("customer_email", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="family",
            fields=[
                ("family_id", models.IntegerField(primary_key=True, serialize=False)),
                ("family_name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="payment_type",
            fields=[
                (
                    "payment_type_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("cash", "Cash"),
                            ("credit_card", "Credit Card"),
                            ("bank_transfer", "bank_transfer"),
                            ("other", "other"),
                        ],
                        max_length=20,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="product",
            fields=[
                ("product_id", models.IntegerField(primary_key=True, serialize=False)),
                ("product_name", models.CharField(max_length=255)),
                ("product_size", models.CharField(max_length=50)),
                ("color", models.CharField(max_length=255)),
                ("product_description", models.TextField()),
                ("product_reference", models.CharField(max_length=10)),
                ("product_price_buy", models.FloatField()),
                ("product_price_sell", models.FloatField()),
                ("product_quantity", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="supplier",
            fields=[
                ("supplier_id", models.IntegerField(primary_key=True, serialize=False)),
                ("supplier_company_name", models.CharField(max_length=255)),
                ("supplier_contact_name", models.CharField(max_length=255)),
                ("supplier_address", models.CharField(max_length=255)),
                ("supplier_region", models.CharField(max_length=255)),
                ("supplier_postal_code", models.CharField(max_length=10)),
                ("supplier_city", models.CharField(max_length=255)),
                ("supplier_phone", models.CharField(max_length=20)),
                ("supplier_email", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="customer_invoice",
            fields=[
                (
                    "customer_invoice_id",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("customer_invoice_date", models.DateField()),
                ("customer_invoice_amount_due", models.FloatField()),
                (
                    "customer_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.customer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="customer_invoice_payment",
            fields=[
                (
                    "customer_invoice_payment_id",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("customer_invoice_payment_date", models.DateField()),
                ("customer_invoice_payment_amount", models.FloatField()),
                (
                    "customer_invoice_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.customer_invoice",
                    ),
                ),
                (
                    "payment_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="inventory.payment_type",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="customer_invoice_item",
            fields=[
                (
                    "customer_invoice_item_id",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("customer_invoice_item_quantity", models.IntegerField()),
                ("customer_invoice_item_price", models.FloatField()),
                ("customer_invoice_item_discount", models.FloatField()),
                (
                    "customer_invoice_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.customer_invoice",
                    ),
                ),
                (
                    "product_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="sub_family",
            fields=[
                (
                    "subfamily_id",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("subfamily_name", models.CharField(max_length=50)),
                (
                    "family",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.family",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="subfamily_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="inventory.sub_family"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="supplier_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="inventory.supplier"
            ),
        ),
        migrations.CreateModel(
            name="supplier_invoice",
            fields=[
                (
                    "supplier_invoice_id",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("supplier_invoice_number", models.CharField(max_length=200)),
                ("supplier_invoice_date", models.DateField()),
                ("supplier_invoice_amount_due", models.FloatField()),
                ("supplier_invoice_image_data", models.BinaryField()),
                (
                    "supplier_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.supplier",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="supplier_invoice_item",
            fields=[
                (
                    "supplier_invoice_item_id",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("supplier_invoice_item_quantity", models.IntegerField()),
                ("supplier_invoice_item_price", models.FloatField()),
                ("supplier_invoice_item_discount", models.FloatField()),
                (
                    "product_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.product",
                    ),
                ),
                (
                    "supplier_invoice_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.supplier_invoice",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="supplier_invoice_payment",
            fields=[
                (
                    "supplier_invoice_payment_id",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("supplier_invoice_payment_date", models.DateField()),
                ("supplier_invoice_payment_amount", models.FloatField()),
                (
                    "payment_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="inventory.payment_type",
                    ),
                ),
                (
                    "supplier_invoice_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.supplier_invoice",
                    ),
                ),
            ],
        ),
    ]
