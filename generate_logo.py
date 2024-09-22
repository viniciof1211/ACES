from PIL import Image, ImageDraw, ImageFont
import io

# Create a 200x200 image with a white background
img = Image.new('RGB', (200, 200), 'white')
draw = ImageDraw.Draw(img)

# Draw the circle with Azure colors
draw.ellipse([5, 5, 195, 195], fill='#0078D4', outline='#005A9E', width=10)

# Draw the Azure Symbol (Polygon)
draw.polygon([(60, 120), (100, 40), (140, 120)], fill='white')
draw.polygon([(95, 105), (105, 105), (115, 130), (85, 130)], fill='#0078D4')

# Draw the Certification Badge
draw.rectangle([55, 130, 145, 160], fill='white', outline='#005A9E', width=2)

# Add the text "CERTIFIED"
font = ImageFont.load_default()
draw.text((100, 145), "CERTIFIED", fill='#0078D4', font=font, anchor="mm")

# Draw the Progress Indicator Icon (circle with check)
draw.ellipse([155, 155, 185, 185], fill='white', outline='#0078D4', width=2)
draw.line([(164, 170), (170, 176), (178, 164)], fill='#0078D4', width=2)

# Add the app name (Bold Italic Dark Blue)
draw.text((100, 190), "Azure Cert\nPractice Simulator", fill='#003366', font=font, anchor="mm")

# Save the image as JPEG to an in-memory file
jpeg_image = io.BytesIO()
img.save(jpeg_image, format='JPEG')

# Reset the stream position to the start
jpeg_image.seek(0)

# Encode the JPEG to a text file
jpeg_encoded_text = jpeg_image.getvalue().hex()

jpeg_encoded_text[:500]  # Returning the first 500 characters for preview
