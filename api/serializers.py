# api/serializers.py

from rest_framework import serializers
from .models import Item, Category, Tag

class TagField(serializers.ListField):
    child = serializers.IntegerField()

    def to_representation(self, data):
        return [tag.name for tag in data.all()]

    def to_internal_value(self, data):
        return [Tag.objects.get_or_create(id=tag_id)[0] for tag_id in data]

class ItemSerializer(serializers.ModelSerializer):
    category = serializers.CharField(max_length=100)
    tags = TagField()  # Change to a ListField that accepts integers (tag IDs)

    class Meta:
        model = Item
        fields = ['SKU', 'name', 'category', 'tags', 'stock_status', 'available_stock']

    def create(self, validated_data):
        category_name = validated_data.pop('category')
        tags_data = validated_data.pop('tags', [])

        category, _ = Category.objects.get_or_create(name=category_name)
        item = Item.objects.create(category=category, **validated_data)
        item.tags.set(tags_data)  # assuming tags_data is a list of Tag instances
        return item


