from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.utils import timezone
from openpyxl import Workbook

from .models import Product


def build_excel(rows):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(['product_id', 'name', 'category', 'price', 'quantity'])
    for row in rows:
        sheet.append(row)
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()


class ProductWorkflowTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_upload_creates_drafts(self):
        excel_bytes = build_excel([
            [101, 'Alpha', 'Books', 9.99, 10],
            [102, 'Beta', 'Electronics', 19.5, 5],
        ])
        upload = SimpleUploadedFile('products.xlsx', excel_bytes, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response = self.client.post('/', {'file': upload})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 2)
        self.assertTrue(Product.objects.filter(status=Product.Status.DRAFT).exists())

    def test_upload_updates_existing_as_draft(self):
        product = Product.objects.create(
            product_id=201,
            name='Old',
            category='Home',
            price=5.00,
            quantity=1,
            status=Product.Status.APPROVED,
        )
        excel_bytes = build_excel([[201, 'New Name', 'Home', 7.25, 3]])
        upload = SimpleUploadedFile('products.xlsx', excel_bytes, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response = self.client.post('/', {'file': upload})
        self.assertEqual(response.status_code, 302)
        product.refresh_from_db()
        self.assertEqual(product.name, 'New Name')
        self.assertEqual(product.price, 7.25)
        self.assertEqual(product.quantity, 3)
        self.assertEqual(product.status, Product.Status.DRAFT)

    def test_approve_changes_status(self):
        product = Product.objects.create(
            product_id=301,
            name='Approve Me',
            category='Sports',
            price=12.00,
            quantity=2,
            status=Product.Status.DRAFT,
        )
        response = self.client.post(f'/approve/{product.product_id}/')
        self.assertEqual(response.status_code, 302)
        product.refresh_from_db()
        self.assertEqual(product.status, Product.Status.APPROVED)

    def test_approved_filters(self):
        Product.objects.create(
            product_id=401,
            name='Running Shoe',
            category='Sports',
            price=40.00,
            quantity=4,
            status=Product.Status.APPROVED,
        )
        Product.objects.create(
            product_id=402,
            name='Desk Lamp',
            category='Home',
            price=15.00,
            quantity=8,
            status=Product.Status.APPROVED,
        )
        Product.objects.filter(product_id=401).update(last_updated=timezone.now() - timezone.timedelta(days=5))
        Product.objects.filter(product_id=402).update(last_updated=timezone.now())

        response = self.client.get('/approved/', {'q': 'Desk'})
        self.assertContains(response, 'Desk Lamp')
        self.assertNotContains(response, 'Running Shoe')

        response = self.client.get('/approved/', {'start_date': (timezone.now() - timezone.timedelta(days=1)).date().isoformat()})
        self.assertContains(response, 'Desk Lamp')
        self.assertNotContains(response, 'Running Shoe')
