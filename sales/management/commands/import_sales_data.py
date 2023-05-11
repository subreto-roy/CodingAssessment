import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from sales.models import Sale

class Command(BaseCommand):
    help = 'Import sales data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transaction_date = datetime.strptime(row['order_date'], '%Y-%m-%d').date()
                Sale.objects.create(
                    order_id=row['order_id'],
                    order_date=transaction_date,
                    ship_date=row['ship_date'],
                    ship_mode=row['ship_mode'],
                    customer_id=row['customer_id'],
                    customer_name=row['customer_name'],
                    segment=row['segment'],
                    country=row['country'],
                    city=row['city'],
                    state=row['state'],
                    postal_code=row['postal_code'],
                    region=row['region'],
                    product_id=row['product_id'],
                    category=row['category'],
                    sub_category=row['sub_category'],
                    product_name=row['product_name'],
                    sales=row['sales'],
                    
                )
        self.stdout.write(self.style.SUCCESS('Sales data imported successfully.'))
