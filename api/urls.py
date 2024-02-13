# api/urls.py
from django.urls import path
from .views import ItemDashboardView
from .views import UserRegistrationView
from .views import LoginView
from .views import ItemListView



urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('item-dashboard/', ItemDashboardView.as_view(), name='item-dashboard'),
    path('item-list/', ItemListView.as_view(), name='item-list'),
    path('item-dashboard/<str:sku>/', ItemDashboardView.as_view(), name='item-delete'),
]
