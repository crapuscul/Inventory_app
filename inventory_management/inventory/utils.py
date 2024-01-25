# utils.py
import os
import re
from django.conf import settings

def generate_sku(product_name, product_id, product_reference):
    # Example: Concatenate the first three characters of product_name, product_id, and product_reference
    name_part = product_name[:3].upper()
    sku = f"{name_part}{product_id}{product_reference}"

    # Print or log the SKU for debugging
    #print(f"SKU before: {sku}")

    # Remove invalid characters using regular expression
    sku = re.sub(r'[^a-zA-Z0-9_-]', '', sku)

    # Print or log the SKU after removing invalid characters
    #print(f"SKU after: {sku}")

    barcode_path = os.path.join(settings.MEDIA_ROOT, f'media/images/barcode_{sku}.png')

    return sku, barcode_path


