from django.test import TestCase
from .models import Item
from .serializers import ItemSerializer

class ItemSerializerTests(TestCase):
    def test_item_serializer(self):
        item_data = {'sku': 'SKU001', 'name': 'Test Item', 'category': 'Test Category', 'tags': 'tag1,tag2', 'stock_status': 'In Stock', 'available_stock': 10}
        serializer = ItemSerializer(data=item_data)
        self.assertTrue(serializer.is_valid())
