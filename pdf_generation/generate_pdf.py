from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf(data):
    print(type(data))
    filename = f"output_{data['uid']}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Set font and size
    c.setFont("Helvetica", 12)
    
    # Fill in template fields from JSON (customize as needed)
    c.drawString(100, 730, f"uid: {data['uid']}")
    c.drawString(100, 750, f"Name: {data['name']}")
    c.drawString(100, 770, f"Email: {data['email']}")
    c.drawString(100, 790, f"sid: {data['sid']}")
    c.drawString(100, 810, f"qty: {data['qty']}")
    c.drawString(100, 830, f"value: {data['value']}")
    
    # More fields from the template can be added here as needed
    
    c.save()
    print(f"PDF saved as {filename}")

