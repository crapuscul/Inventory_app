# Django inventory app models

from django.db import models

from .utils import generate_sku
import os
from barcode.writer import ImageWriter
from django.conf import settings
from barcode import generate

from barcode.errors import BarcodeError

class family(models.Model):
    family_id = models.AutoField(primary_key=True)
    family_name = models.CharField(max_length=50)

    def __str__(self):
        return self.family_name

class subfamily(models.Model):
    subfamily_id = models.AutoField(primary_key=True)
    subfamily_name = models.CharField(max_length=50)
    family = models.ForeignKey(family, on_delete=models.CASCADE)
    def __str__(self):
        return self.subfamily_name
    
from srm.models import supplier

class product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_size = models.CharField(max_length=50)
    color = models.CharField(max_length=255)
    product_description = models.TextField()
    supplier_id = models.ForeignKey(supplier, on_delete=models.CASCADE, null=True)
    product_reference = models.CharField(max_length = 10)
    product_price_buy = models.FloatField(null=True)
    product_price_sell = models.FloatField(null=True)
    product_quantity = models.IntegerField(null=True)
    subfamily = models.ForeignKey(subfamily, on_delete=models.CASCADE, null=True)
    barcode = models.ImageField(upload_to='images/', null=True, blank=True)
    sku = models.CharField(max_length=20, blank=True, null=True)




    def save(self, *args, **kwargs):
        if not self.sku:
            # Generate SKU
            self.sku, _ = generate_sku(self.product_name, self.product_id, self.product_reference)

        # Set the barcode field
        barcode_filename = f"barcode_{self.sku}.png"
        barcode_path = os.path.join(settings.MEDIA_ROOT, 'images', barcode_filename)
        self.barcode.name = barcode_path

        if not self.barcode:
            # Generate Barcode
            barcode_string = generate('Code128', self.sku, writer=ImageWriter(), output=barcode_path)

            with open(barcode_path, 'wb') as barcode_file:
                barcode_file.write(barcode_string)

            # Update the barcode field after saving the product
            self.barcode.name = barcode_path

        super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return f"{self.product_name} - SKU: {self.sku}"


    
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




class customer(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    customer_city = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.CharField(max_length=255)

class customer_invoice(models.Model):
    customer_invoice_id = models.IntegerField(primary_key=True)
    customer_id = models.ForeignKey(customer, on_delete=models.CASCADE)
    customer_invoice_date = models.DateField()
    customer_invoice_amount_due = models.FloatField()

class customer_invoice_item(models.Model):
    customer_invoice_item_id = models.IntegerField(primary_key=True)
    customer_invoice_id = models.ForeignKey(customer_invoice, on_delete=models.CASCADE)
    product_id = models.ForeignKey(product, on_delete=models.CASCADE)
    customer_invoice_item_quantity = models.IntegerField()
    customer_invoice_item_price = models.FloatField()
    customer_invoice_item_discount = models.FloatField()

class customer_invoice_payment(models.Model):
    customer_invoice_payment_id = models.IntegerField(primary_key=True)
    customer_invoice_id = models.ForeignKey(customer_invoice, on_delete=models.CASCADE)
    customer_invoice_payment_date = models.DateField()
    customer_invoice_payment_amount = models.FloatField()
    payment_type = models.ForeignKey(payment_type, on_delete=models.SET_NULL, null=True, blank=True)
    
class Transaction(models.Model):
    products = models.ManyToManyField(product)
    timestamp = models.DateTimeField(auto_now_add=True)