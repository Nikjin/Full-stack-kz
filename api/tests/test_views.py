from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Item

class ItemDashboardViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='testpassword')
        self.client.login(username='test_user', password='testpassword')
        self.item = Item.objects.create(sku='SKU001', name='Test Item', category='Test Category', tags='tag1,tag2', stock_status='In Stock', available_stock=10)

    def test_get_items(self):
        url = reverse('item-dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['sku'], 'SKU001')

    # Add more test cases for ItemDashboardView as needed

class ItemListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='testpassword')
        self.client.login(username='test_user', password='testpassword')
        self.item1 = Item.objects.create(sku='SKU001', name='Test Item 1', category='Test Category', tags='tag1,tag2', stock_status='In Stock', available_stock=10)
        self.item2 = Item.objects.create(sku='SKU002', name='Test Item 2', category='Test Category', tags='tag1,tag2', stock_status='Out of Stock', available_stock=0)

    def test_get_items(self):
        url = reverse('item-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # Add more test cases for ItemListView as needed

# Add similar test cases for other views if needed
