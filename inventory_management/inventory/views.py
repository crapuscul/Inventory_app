from django.shortcuts import render, get_object_or_404, redirect
from .models import product, family, subfamily
from srm.models import supplier
from .forms import ProductForm, FamilyForm, SubFamilyForm, SubFamilyEditForm

#import logging
from django.http import HttpResponseBadRequest
from barcode.writer import ImageWriter
from .utils import generate_sku
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
from barcode import Code128
from io import BytesIO
import base64
from barcode.errors import BarcodeError
import os
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas






#index:
def index(request):
    return render(request,'inventory/index.html')

#family_list:
def family_list(request):
    families = family.objects.all()
    return render(request,'inventory/family_list.html', {'families': families})

#subfamily_list
def subfamily_list(request):
    subfamilies = subfamily.objects.all()
    return render(request, 'inventory/subfamily_list.html', {'subfamilies': subfamilies})


#add_family:
def add_family(request):
    if request.method == 'POST':
        family_form = FamilyForm(request.POST)
        if family_form.is_valid():
            family_form.save()
            return redirect('inventory:family_list')
    else:
        family_form = FamilyForm()
    return render(request, 'inventory/add_family.html',{'family_form':family_form})

#logger = logging.getLogger(__name__)

def add_subfamily(request):
    if request.method == 'POST':
        subfamily_form = SubFamilyForm(request.POST, prefix='subfamily')
        #logger.error(request.POST)  # Logging line

        if subfamily_form.is_valid():
            subfamily_instance = subfamily_form.save(commit=False)

            # Get the family instance ID from the form data
            family_instance_id = request.POST.get('subfamily-family')
            #logger.error(f"Family instance ID: {family_instance_id}")  # Logging line

            if family_instance_id is None:
                return HttpResponseBadRequest("Missing 'subfamily-family' field in form data.")

            # Retrieve the corresponding family instance
            family_instance = get_object_or_404(family, pk=family_instance_id)

            subfamily_instance.family = family_instance
            subfamily_instance.save()
            return redirect('inventory:family_list')  # Redirect wherever appropriate

    else:
        subfamily_form = SubFamilyForm(prefix='subfamily')

    return render(request, 'inventory/add_subfamily.html', {'subfamily_form': subfamily_form})

#Product_list:
def product_list(request):
    products = product.objects.all()
    return render(request,'inventory/product_list.html', {'products': products})

#add_product:


def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, prefix='product')
        if product_form.is_valid():
            family_id = request.POST.get('product-family')
            subfamily_id = request.POST.get('product-subfamily')
            supplier_id = request.POST.get('product-supplier')

            try:
                family_instance = family.objects.get(pk=family_id)
            except family.DoesNotExist:
                print(f"DEBUG: Family with ID {family_id} does not exist.")
                return HttpResponseBadRequest("Selected family does not exist.")

            try:
                subfamily_instance = subfamily.objects.get(pk=subfamily_id)
            except subfamily.DoesNotExist:
                print(f"DEBUG: SubFamily with ID {subfamily_id} does not exist.")
                return HttpResponseBadRequest("Selected subfamily does not exist.")
            try:
                supplier_instance = supplier.objects.get(pk=supplier_id)
            except supplier.DoesNotExist:
                print(f"DEBUG: Supplier with ID {supplier_id} does not exist.")
                return HttpResponseBadRequest("Selected supplier does not exist.")
            

            product_instance = product_form.save(commit=False)
            product_instance.family = family_instance
            product_instance.subfamily = subfamily_instance
            product_instance.supplier = supplier_instance

            product_instance.save()

            return redirect('inventory:product_list')

        else:
            return HttpResponseBadRequest("Invalid form data. Please check the submitted information.")

    else:
        product_form = ProductForm(prefix='product')

    return render(request, 'inventory/add_product.html', {'product_form': product_form})

#edit_subfamily:
def edit_subfamily(request, pk):
    subfamily_instance = get_object_or_404(subfamily, pk=pk)
    if request.method == 'POST':
        subfamily_form = SubFamilyEditForm(request.POST, instance=subfamily_instance)
        if subfamily_form.is_valid():
            subfamily_form.save()
            return redirect('inventory:subfamily_list')
    else:
        subfamily_form = SubFamilyEditForm(instance=subfamily_instance)
    return render(request, 'inventory/edit_subfamily.html',{'subfamily_form':subfamily_form,'subfamily_instance': subfamily_instance})


#delete_subfamily:
def delete_subfamily(request, pk):
    subfamily_instance = get_object_or_404(subfamily, pk=pk)

    if request.method == 'POST':
        subfamily_instance.delete()
        return redirect ('inventory:subfamily_list')

    return render(request, 'inventory/delete_subfamily.html', {'subfamily': subfamily_instance})


#edit_product:
def edit_product(request,pk):
    prod_instance = get_object_or_404(product, pk = pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=prod_instance)
        if form.is_valid():
            form.save()
            return redirect('inventory:product_list')
    else:
        form = ProductForm(instance=prod_instance)
    return render(request, 'inventory/edit_product.html',{'form':form,'product': prod_instance})

#delete_product:

def delete_product(request, pk):
    prod_instance = get_object_or_404(product, pk = pk)

    if request.method == 'POST':
        prod_instance.delete()
        return redirect('inventory:product_list')

    return render(request, 'inventory/delete_product.html', {'product': prod_instance})


def generate_label(request, pk):
    try:
        # Retrieve the product based on the product_id
        product_instance = get_object_or_404(product, pk=pk)

        # Generate SKUlabe
        sku, _ = generate_sku(product_instance.product_name, product_instance.product_id, product_instance.product_reference)

        # Create an image for the label
        label_image = generate_label_image(product_instance, sku)

        if label_image is None:
            # Handle the case where barcode generation fails
            return HttpResponse("Barcode generation failed. Please check your data.")

        # Save the label image to BytesIO
        label_image_buffer = BytesIO()
        label_image.save(label_image_buffer, format='PNG')
        label_image_buffer.seek(0)

        # Save the label image to a file on the server

        

        # Encode the label image to base64
        barcode_image_base64 = base64.b64encode(label_image_buffer.read()).decode('utf-8')

        # Pass the image and SKU directly to the print_label function
        if 'print' in request.GET:
            return print_label(request, pk, product_instance, sku=sku)

        context = {
            'product': product_instance,
            'sku': sku,
            'label_image_base64': barcode_image_base64,
        }

        return render(request, 'inventory/generate_label_preview.html', context)

    except BarcodeError as e:
        # Handle BarcodeError
        return HttpResponse(f"Barcode generation failed. Error: {e}")
    except Exception as e:
        # Handle other unexpected errors
        return HttpResponse(f"An unexpected error occurred. Error: {e}")
    
    

def print_label(request, pk, product_instance, sku, dpi=600):
    try:
        product_instance = product.objects.get(pk=pk)

        # Generate the label image
        label_image = generate_label_image(product_instance, sku, dpi)

        # Create a PDF document
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="labels_{pk}.pdf"'

        # Create a canvas for drawing on the PDF
        p = canvas.Canvas(response, pagesize=(label_image.width, label_image.height))


        label_image_path = os.path.join(settings.MEDIA_ROOT, 'images', f"label_{sku}.png")
        label_image.save(label_image_path, format='PNG')
        p.drawInlineImage(label_image, 0,0)


        # Close the PDF canvas
        p.save()



        return response
    

    except product.DoesNotExist:
        return HttpResponse("Product not found.")
    except Exception as e:
        return HttpResponse(f"An unexpected error occurred. Error: {e}")


def generate_label_image(product_instance, sku, dpi=600):
    # Calculate the size of the image in inches based on the desired DPI
    width_inches = 1600 / dpi
    height_inches = 804 / dpi

    # Create an image for the label with higher DPI
    image = Image.new('RGBA', (int(width_inches * dpi), int(height_inches * dpi)), (255, 255, 255, 255))
    # Set the DPI of the image
    image.info['dpi'] = (dpi, dpi)

    # Generate the barcode with Code 128
    barcode_value = sku
    code128 = Code128(barcode_value, writer=ImageWriter())

    # Render the barcode and draw it on the image
    barcode_image = code128.render()
    barcode_image = barcode_image.convert('RGBA')

    # Resize the barcode image to fit the label dimensions
    barcode_image = barcode_image.resize((int(1200), int(600)))

    # Draw the barcode on the image
    image.paste(barcode_image, (int(40 * dpi / 72), int(20 * dpi / 72)))

    # Load fonts for text
    font_prod_name = ImageFont.truetype('arial.ttf', size=int(10 * dpi / 72))
    font_price_ref = ImageFont.truetype('arialbd.ttf', size=int(16 * dpi / 72))

    # ... (rest of the function)

    # Rotate and paste vertically oriented text (Product Name)
    rotated_text_product_name = Image.new('RGBA', (int(75 * dpi / 72), int(125 * dpi / 72)), (255, 255, 255, 0))
    rotated_draw_product_name = ImageDraw.Draw(rotated_text_product_name)
    rotated_draw_product_name.text((0, 0), f"{product_instance.product_name}", font=font_prod_name, fill='black')
    rotated_text_product_name = rotated_text_product_name.rotate(270, expand=True)
    image.paste(rotated_text_product_name, (int(-84 * dpi / 72), int(30 * dpi / 72)), rotated_text_product_name)

    # Rotate and paste vertically oriented text (Price Sell)
    rotated_text_price_sell = Image.new('RGBA', (int(120 * dpi / 72), int(200 * dpi / 72)), (255, 255, 255, 0))
    rotated_draw_price_sell = ImageDraw.Draw(rotated_text_price_sell)
    rotated_draw_price_sell.text((0, 0), f"{product_instance.product_price_sell}", font=font_price_ref, fill='black')
    rotated_text_price_sell = rotated_text_price_sell.rotate(270, expand=True)
    image.paste(rotated_text_price_sell, (int(-180 * dpi / 72), int(50 * dpi / 72)), rotated_text_price_sell)

    # Rotate and paste vertically oriented text (Product Reference)
    rotated_text_ref = Image.new('RGBA', (int(120 * dpi / 72), int(200 * dpi / 72)), (255, 255, 255, 0))
    rotated_draw_ref = ImageDraw.Draw(rotated_text_ref)
    rotated_draw_ref.text((0, 0), f"{product_instance.product_reference}", font=font_price_ref, fill='black')
    rotated_text_ref = rotated_text_ref.rotate(270, expand=True)
    image.paste(rotated_text_ref, (int(-180 * dpi / 72), int(5 * dpi / 72)), rotated_text_ref)

    # Calculate the position for the line to be between the product name and barcode
    line_position = (int(-10 * dpi / 72), 0)
    line_width = int(100 * dpi / 72)
    line_height = int(150 * dpi / 72)
    line_middle = line_width // 2

    # Draw a line on the image
    draw_line = ImageDraw.Draw(image)
    line_coordinates = (
        
            line_position[0] + line_middle,
            line_position[1],
            line_position[0] + line_middle,
            line_position[1] + line_height
    
    )
    line_color = 'black'
    line_thickness = 10  # Adjust the thickness as needed
    draw_line.line(line_coordinates, fill=line_color, width=line_thickness)

# Calculate the position for the second line to be vertical
    line2_position = (0, 250)
    line2_width = int( 260)
    line2_height = int(100 * dpi / 72)
    line2_middle = line2_width // 2

# Draw the second line on the image
    draw_line2 = ImageDraw.Draw(image)
    line2_coordinates = (
        line2_position[0],
        line2_position[1] + line2_middle,
        line2_position[0] + line2_width,
        line2_position[1] + line2_middle
    )
    line2_color = 'black'
    line2_thickness = 10  # Adjust the thickness as needed

    draw_line2.line(line2_coordinates, fill=line2_color, width=line2_thickness)

    return image

    return image
