# api/serializers.py

from rest_framework import serializers
from .models import Item, Category, Tag
import logging

# Create a logger for this file
logger = logging.getLogger(__name__)

class TagField(serializers.ListField):
    child = serializers.CharField()

    def to_representation(self, data):
        # Represent tags as a list of their names
        return [tag.name for tag in data.all()]

    def to_internal_value(self, data):
        # Process each tag identifier (name in this case) to ensure valid Tag objects
        tags = []
        for tag_name in data:
            if tag_name:  # Ensure non-empty tag name
                tag, created = Tag.objects.get_or_create(name=tag_name.strip())  # Create tag based on name
                tags.append(tag)
            else:
                raise serializers.ValidationError("Tag names cannot be empty.")
        return tags

class ItemSerializer(serializers.ModelSerializer):
    category = serializers.CharField(max_length=100)
    tags = TagField()

    class Meta:
        model = Item
        fields = ['SKU', 'name', 'category', 'tags', 'stock_status', 'available_stock']

    def create(self, validated_data):
        category_name = validated_data.pop('category')
        tags_data = validated_data.pop('tags', [])

        category, _ = Category.objects.get_or_create(name=category_name)
        item = Item.objects.create(category=category, **validated_data)
        item.tags.set(tags_data)  # Associate the item with the tags

        return item

