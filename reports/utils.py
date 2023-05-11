from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_pdf_report(data):
    # Create a BytesIO object to write the PDF content
    buffer = BytesIO()

    # Create the PDF canvas
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Set the font and font size
    pdf.setFont("Helvetica", 12)

    # Write the content to the PDF
    pdf.drawString(50, 750, "My PDF Report")
    pdf.drawString(50, 700, f"Total Orders: {data['total_orders']}")
    pdf.drawString(50, 650, f"Distinct Customers: {data['distinct_customers']}")

    # ... Add more content to the PDF ...

    # Save the PDF canvas
    pdf.save()

    # Move the buffer's pointer to the beginning
    buffer.seek(0)

    # Return the PDF content as bytes
    return buffer.getvalue()
