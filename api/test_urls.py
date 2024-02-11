from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import ItemDashboardView, ItemListView, UserRegistrationView, LoginView

class TestUrls(SimpleTestCase):
    def test_item_dashboard_url_resolves(self):
        url = reverse('item-dashboard')
        self.assertEqual(resolve(url).func.view_class, ItemDashboardView)

    def test_item_list_url_resolves(self):
        url = reverse('item-list')
        self.assertEqual(resolve(url).func.view_class, ItemListView)

    def test_user_registration_url_resolves(self):
        url = reverse('user-registration')
        self.assertEqual(resolve(url).func.view_class, UserRegistrationView)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)
