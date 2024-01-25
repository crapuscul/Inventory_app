from django.db import models

# Create your models here.
class supplier(models.Model):
    supplier_id = models.IntegerField(primary_key=True)
    supplier_name = models.CharField(max_length=255)
    supplier_contact_name = models.CharField(max_length=255)
    supplier_address = models.CharField(max_length=255)
    supplier_region = models.CharField(max_length=255)
    supplier_postal_code = models.CharField(max_length=10)
    supplier_city = models.CharField(max_length=255)
    supplier_phone = models.CharField(max_length=20)
    supplier_email = models.CharField(max_length=255)

    def __str__(self):
        return self.supplier_name

class supplier_invoice(models.Model):
    supplier_invoice_id = models.IntegerField(primary_key=True)
    supplier_invoice_number = models.CharField(max_length=200)
    supplier_invoice_date = models.DateField()
    supplier_id = models.ForeignKey(supplier, on_delete=models.CASCADE)
    supplier_invoice_amount_due = models.FloatField()
    supplier_invoice_image_data = models.BinaryField()
from inventory.models import product

class supplier_invoice_item(models.Model):
    supplier_invoice_item_id = models.IntegerField(primary_key=True)
    supplier_invoice_id = models.ForeignKey(supplier_invoice, on_delete=models.CASCADE)
    product_id = models.ForeignKey(product, on_delete=models.CASCADE)
    supplier_invoice_item_quantity = models.IntegerField()
    supplier_invoice_item_price = models.FloatField()
    supplier_invoice_item_discount = models.FloatField()


class payment_type(models.Model):
    cash = 'cash'
    credit_card = 'credit_card'
    bank_transfer = 'bank_transfer'
    other = 'other'

    payment_type_choices = [
        (cash, 'Cash'),
        (credit_card, 'Credit Card'),
        (bank_transfer,'bank_transfer'),
        (other, 'other'),
    ]

    payment_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, choices=payment_type_choices, unique=True)

    def __str__(self):
        return self.get_name_display()

class supplier_invoice_payment(models.Model):
    supplier_invoice_payment_id = models.IntegerField(primary_key=True)
    supplier_invoice_id = models.ForeignKey(supplier_invoice, on_delete=models.CASCADE)
    supplier_invoice_payment_date = models.DateField()
    supplier_invoice_payment_amount = models.FloatField()
    payment_type = models.ForeignKey(payment_type, on_delete=models.SET_NULL, null=True, blank=True)

