# api/serializers.py

from rest_framework import serializers
from .models import Item, Category, Tag

class ItemSerializer(serializers.ModelSerializer):
    category = serializers.CharField(write_only=True)
    tags = serializers.ListField(write_only=True)

    class Meta:
        model = Item
        fields = ['SKU', 'name', 'category', 'tags', 'stock_status', 'available_stock']

    def create(self, validated_data):
        category_data = validated_data.pop('category', None)
        tags_data = validated_data.pop('tags', [])

        # Create or get Category instance
        category, _ = Category.objects.get_or_create(name=category_data)

        # Create Tag instances
        tags = [Tag.objects.get_or_create(name=tag_data)[0] for tag_data in tags_data]

        # Create Item instance with the related Category and Tags
        instance = Item.objects.create(category=category, **validated_data)
        instance.tags.set(tags)

        return instance
