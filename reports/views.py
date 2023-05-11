from io import BytesIO
from tkinter import Canvas
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.db.models import Count
from sales.models import Sale
import matplotlib.pyplot as plt
import pandas as pd
from reportlab.pdfgen import canvas

def generate_report(request):
    # Fetch the dataset from the database or some other source
    dataset = Sale.objects.all()  # Adjust this based on your model and dataset retrieval method

    # Create a PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # Create a PDF object
    pdf = Canvas.Canvas(response)

    # Total number of orders count per year
    orders_per_year = dataset.values('order_date__year').annotate(count=Count('id')).order_by('order_date__year')
    pdf.drawString(50, 800, "Total Number of Orders per Year:")
    y_position = 780
    for order in orders_per_year:
        year = order['order_date__year']
        count = order['count']
        pdf.drawString(70, y_position, f"{year}: {count}")
        y_position -= 20

    # Total count of distinct customers
    distinct_customers = dataset.values('customer_id').distinct().count()
    pdf.drawString(50, y_position, f"Total Count of Distinct Customers: {distinct_customers}")
    y_position -= 40

    # Top 3 customers who have ordered the most with their total amount of transactions
    top_customers = dataset.values('customer_id').annotate(total_transactions=Count('id')).order_by(
        '-total_transactions')[:3]
    pdf.drawString(50, y_position, "Top 3 Customers with Most Orders:")
    y_position -= 20
    for customer in top_customers:
        customer_id = customer['customer_id']
        total_transactions = customer['total_transactions']
        pdf.drawString(70, y_position, f"Customer ID: {customer_id}, Total Transactions: {total_transactions}")
        y_position -= 20

    # Customer Transactions per Year (from the beginning year to last year)
    customer_transactions = dataset.values('customer_id', 'order_date__year').annotate(
        count=Count('id')).order_by('customer_id', 'order_date__year')
    pdf.drawString(50, y_position, "Customer Transactions per Year:")
    y_position -= 20
    current_customer = None
    for transaction in customer_transactions:
        customer_id = transaction['customer_id']
        year = transaction['order_date__year']
        count = transaction['count']
        if customer_id != current_customer:
            pdf.drawString(70, y_position, f"Customer ID: {customer_id}")
            y_position -= 20
            current_customer = customer_id
        pdf.drawString(90, y_position, f"{year}: {count}")
        y_position -= 20

    # Most selling items sub-category names
    top_subcategories = dataset.values('sub_category').annotate(count=Count('id')).order_by('-count')[:5]
    pdf.drawString(50, y_position, "Most Selling Sub-Category Names:")
    y_position -= 20
    for subcategory in top_subcategories:
        sub_category = subcategory['sub_category']
        count = subcategory['count']
        pdf.drawString(70, y_position, f"{sub_category}: {count}")
        y_position -= 20

    # Region basis sales performance pie chart
    sales_per_region = dataset.values('region').annotate(sales=Count('id')).order_by('-sales')
    regions = [region['region'] for region in sales_per_region]
    sales = [region['sales'] for region in sales_per_region]

    # Generate a pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(sales, labels=regions, autopct='%1.1f%%')
    plt.title('Region Sales Performance')

    # Save the pie chart to a BytesIO object
    chart_buffer = BytesIO()
    plt.savefig(chart_buffer, format='png')
    plt.close()

    # Set the chart buffer position to the start
    chart_buffer.seek(0)

    # Add the pie chart to the PDF document
    pdf.drawInlineImage(chart_buffer, 100, y_position - 120, width=300, height=300)

    # Sales performance line chart over the years
    sales_per_year = dataset.values('order_date__year').annotate(total_sales=Count('id')).order_by('order_date__year')
    years = [sale['order_date__year'] for sale in sales_per_year]
    total_sales = [sale['total_sales'] for sale in sales_per_year]

    # Generate a line chart
    plt.figure(figsize=(10, 6))
    plt.plot(years, total_sales, marker='o')
    plt.xlabel('Year')
    plt.ylabel('Total Sales')
    plt.title('Sales Performance over the Years')

    # Save the line chart to a BytesIO object
    chart_buffer = BytesIO()
    plt.savefig(chart_buffer, format='png')
    plt.close()

    # Set the chart buffer position to the start
    chart_buffer.seek(0)

    # Add the line chart to the PDF document
    pdf.drawInlineImage(chart_buffer, 50, y_position - 480, width=500, height=300)

    # Save the PDF document
    pdf.save()

    return response

