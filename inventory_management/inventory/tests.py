# # tests.py
# import os
# from django.test import TestCase
# from .models import product
# from .utils import generate_sku
# from barcode import generate
# from barcode import Code128

# import barcode
# from barcode.writer import ImageWriter
# from PIL import Image, ImageDraw, ImageFont, ImageOps
# from django.conf import settings

# class ProductTestCase(TestCase):
#     def setUp(self):
#         # Create a sample product instance for testing
#         self.product = product.objects.create(
#             product_id=1,
#             product_name="Test Product",
#             product_reference="ABO",
#             product_price_buy=10.99,
#             product_price_sell=19.99,
#             product_quantity=100,
#         )

#     def test_generate_sku(self):
#         # Test SKU generation logic
#         sku, _ = generate_sku(self.product.product_name, self.product.product_id, self.product.product_reference)
#         expected_sku = "Tes1123"  # Replace with the expected SKU based on your generate_sku logic
#         self.assertEqual(sku, expected_sku)

#     def test_barcode_generation(self):
#         barcode_path = os.path.join(settings.MEDIA_ROOT, 'images', f'barcode_{self.product.sku}.png')

#         # Generate the barcode with Code 128
#         barcode_value = self.product.sku
#         code128 = Code128(barcode_value, writer=ImageWriter())

#         # Create an image with the barcode
#         image = Image.new('RGB', (188, 94), 'white')  # Set the image size as needed
#         #draw = ImageDraw.Draw(image)

#         # Render the barcode and draw it on the image
#         barcode_image = code128.render()
#         barcode_image = barcode_image.convert('RGB')
#         barcode_image = barcode_image.resize((141, 97))
#        # barcode_position = ((image.width - barcode_image.width) // 2, (image.height - barcode_image.height) // 2)
#         image.paste(barcode_image, (40, 8))  # Adjust the position as needed

#         # Load a font
#         font_price_ref = ImageFont.truetype('arialbd.ttf', size=14)  # Change 'arial.ttf' to the path of your font file
#         font_prod_name = ImageFont.truetype('arial.ttf', size=10)


#         # Rotate and paste vertically oriented text
#         rotated_text_product_name = Image.new('RGBA', (75, 125), (255, 255, 255, 0))  # Transparent background
#         rotated_draw_product_name = ImageDraw.Draw(rotated_text_product_name)
#         rotated_draw_product_name.text((0, 0), f"{self.product.product_name}", font=font_prod_name, fill='black')
#         rotated_text_product_name = rotated_text_product_name.rotate(270, expand=True)
#         image.paste(rotated_text_product_name, (-85, 20), rotated_text_product_name)




#         rotated_text_price_sell = Image.new('RGBA', (120, 200), (255, 255, 255, 0))  # Transparent background
#         rotated_draw_price_sell = ImageDraw.Draw(rotated_text_price_sell)
#         rotated_draw_price_sell.text((0, 0), f"{self.product.product_price_sell}", font=font_price_ref, fill='black')
#         rotated_text_price_sell = rotated_text_price_sell.rotate(270, expand=True)
#         image.paste(rotated_text_price_sell, (-180, 50), rotated_text_price_sell)


#         rotated_text_ref = Image.new('RGBA', (120, 200), (255, 255, 255, 0))  # Transparent background
#         rotated_draw_ref = ImageDraw.Draw(rotated_text_ref)
#         rotated_draw_ref.text((0, 0), f"{self.product.product_reference}", font=font_price_ref, fill='black')
#         rotated_text_ref = rotated_text_ref.rotate(270, expand=True)
#         image.paste(rotated_text_ref, (-180, 10), rotated_text_ref)
#        # position_x = (70,35) # get the barcode position
#        # position_y = (-120, -35) # get the pproduct_name_position
#         # Calculate the position for the line to be between the product name and barcode

#         line_position = (-10,0)
#        # line_position = (
#         #    position_y[0] + (position_x[0] - position_y[0] - -110) // 2,
#          #   (position_y[1] + position_x[1]) // 2
#     #)       
#         line_width = 100
#         line_height = 150
#         line_middle = line_width //2

#         draw_line = ImageDraw.Draw(image)
#         draw_line.line(
#             (
#                 line_position[0] + line_middle,
#                 line_position[1],
#                 line_position[0] + line_middle,
#                 line_position[1] + line_height
#             ),
#             fill='black'
#         )


#         # Save the modified image 
#         image.save(barcode_path)


#         # Check if the barcode image file was created
#         self.assertTrue(os.path.isfile(barcode_path))

#         # Optional: Uncomment the line below to open the generated image for manual inspection
#         image.show()


#     def tearDown(self):
#         # Clean up: Delete the created barcode image file
#         barcode_path = os.path.join(settings.MEDIA_ROOT, 'images', f'barcode_{self.product.sku}.png')
#         if os.path.isfile(barcode_path):
#             os.remove(barcode_path)

# # Add more tests as needed
