from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Item

class UserRegistrationViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_with_valid_data(self):
        url = reverse('api/register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Assuming redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_with_missing_fields(self):
        url = reverse('api/register')
        data = {
            'username': '',  # Missing username
            'email': 'incomplete@example.com',
            'password': 'incomplete'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_existing_username(self):
        existing_user = User.objects.create_user('existinguser', 'existing@example.com', 'existingpassword')
        url = reverse('api/register')
        data = {
            'username': 'existinguser',
            'email': 'newemail@example.com',
            'password': 'newpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

# Note: Update 'user-registration' in reverse() function with the actual name of the registration URL as defined in urls.py


class LoginViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='loginuser', email='loginuser@example.com', password='loginpassword')

    def test_login_with_valid_credentials(self):
        url = reverse('api/login')  # Update with the actual URL name
        data = {
            'username': 'loginuser',
            'password': 'loginpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Assuming successful login returns 200 OK

    def test_login_with_invalid_credentials(self):
        url = reverse('api/login')  # Update with the actual URL name
        data = {
            'username': 'loginuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Assuming unauthorized login attempt returns 401


class ItemDashboardViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='testpassword')
        self.client.login(username='test_user', password='testpassword')
        self.item = Item.objects.create(sku='SKU001', name='Test Item', category='Test Category', tags='tag1,tag2', stock_status='In Stock', available_stock=10)

    def test_get_items(self):
        url = reverse('api/item-dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['sku'], 'SKU001')

    def test_create_item(self):
        url = reverse('api/item-dashboard')
        data = {
            'SKU': 'NEW_SKU',
            'name': 'New Item',
            'category': 'New Category',
            'tags': 'tag1,tag2',
            'stock_status': 'In Stock',
            'available_stock': 5
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(Item.objects.last().sku, 'NEW_SKU')

    def test_update_item(self):
        item_update_url = reverse('api/item-dashboard', args=[self.item.id])  # Adjust URL as needed
        updated_data = {
            'name': 'Updated Item Name',
            'category': 'Updated Category',
            'tags': 'updated,tag3',
            'stock_status': 'Out of Stock',
            'available_stock': 0
        }
        response = self.client.put(item_update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Updated Item Name')




class ItemListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='testpassword')
        self.client.login(username='test_user', password='testpassword')
        self.item1 = Item.objects.create(sku='SKU001', name='Test Item 1', category='Test Category', tags='tag1,tag2', stock_status='In Stock', available_stock=10)
        self.item2 = Item.objects.create(sku='SKU002', name='Test Item 2', category='Test Category', tags='tag1,tag2', stock_status='Out of Stock', available_stock=0)

    def test_get_items(self):
        url = reverse('api/item-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_items_by_category(self):
        filter_url = reverse('api/item-list') + '?category=Test Category'
        response = self.client.get(filter_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming all items in the test setup belong to 'Test Category'
        self.assertEqual(len(response.data), 2)
        for item_data in response.data:
            self.assertEqual(item_data['category'], 'Test Category')



