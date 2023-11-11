import json
from PIL import Image, ImageDraw, ImageFont
import random

COMPANY_ADDRESS = "123 Main St"
COMPANY_PHONE = "+1 234 567 890"
COMPANY_EMAIL = "info@example.com"

# Function to generate random receipt entries
def generate_random_receipt_entries(num_entries=5):
    items = ['Apple', 'Banana', 'Milk', 'Bread', 'Cheese', 'Eggs', 'Coffee', 'Tea', 'Juice']
    entries = []
    total_price = 0.0

    for _ in range(num_entries):
        item = random.choice(items)
        qty = random.randint(1, 5)
        price_per_item = round(random.uniform(0.5, 5), 2)
        total_item_price = round(qty * price_per_item, 2)
        total_price += total_item_price
        entries.append((item, qty, price_per_item, total_item_price))

    return entries, round(total_price, 2)

# Function to generate a more "official" looking receipt image
def generate_official_receipt_image(entries, total_price):
    # Create an image with white background
    img = Image.new('RGB', (400, 600), 'white')
    d = ImageDraw.Draw(img)

    # Load a truetype or opentype font file, and create a font object.
    try:
        fnt = ImageFont.truetype('fake receipt.otf', 12)
        fntTitle = ImageFont.truetype('fake receipt.otf', 16)
    except IOError:
        fnt = ImageFont.load_default()
        fntTitle = ImageFont.load_default()

    # Positioning variables
    x, y = 10, 10

    # Draw static text on the image for company name and contact details
    d.text((x, y), "Company Name", font=fntTitle, fill=(0, 0, 0))
    y += 30
    d.text((x, y), f"Address: {COMPANY_ADDRESS}", font=fnt, fill=(0, 0, 0))
    y += 30
    d.text((x, y), f"Phone: {COMPANY_PHONE}", font=fnt, fill=(0, 0, 0))
    y += 30
    d.text((x, y), f"Email: {COMPANY_EMAIL}", font=fnt, fill=(0, 0, 0))
    y += 50

    # Draw text for the receipt items
    d.text((x, y), "Receipt", font=fntTitle, fill=(0, 0, 0))
    y += 30

    for item, qty, price_per_item, total_item_price in entries:
        d.text((x, y), f"{item} x{qty} @ ${price_per_item} = ${total_item_price}", font=fnt, fill=(0, 0, 0))
        y += 30

    # Add VAT and total
    vat = round(total_price * 0.1, 2)  # Assuming 10% VAT
    final_total = round(total_price + vat, 2)

    y += 20
    d.text((x, y), f"VAT: ${vat}", font=fntTitle, fill=(0, 0, 0))
    y += 30
    d.text((x, y), f"Total: ${final_total}", font=fntTitle, fill=(0, 0, 0))

    return img

def generate_random_receipts(num_receipts:int=5, name_prefix:str = 'receipt_'):
    for index in range(num_receipts):
        # Generate random receipt entries
        entries, total_price = generate_random_receipt_entries()

        # Generate official receipt image
        official_img = generate_official_receipt_image(entries, total_price)

        official_img.save(f"{name_prefix}{index+1}.png")
        with open(f"{name_prefix}{index+1}.json", "w") as values_out:
            information = {
                "total": total_price,
                "entries": entries,
            }
            values_out.write(json.dumps(information, indent=4))
