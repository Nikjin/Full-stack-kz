from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
            app_label = 'api'
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
            app_label = 'api'
    def __str__(self):
        return self.name

class Item(models.Model):
    SKU = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    STOCK_STATUS_CHOICES = (
        ('In Stock', 'In Stock'),
        ('Low Stock', 'Low Stock'),
        ('Out of Stock', 'Out of Stock'),
    )
    stock_status = models.CharField(max_length=20, choices=STOCK_STATUS_CHOICES)
    available_stock = models.IntegerField()

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, sku, name, category, tags, stock_status, available_stock):
        item = cls(SKU=sku, name=name, category=category, stock_status=stock_status, available_stock=available_stock)
        item.save()
        item.tags.set(tags)
        return item

    def update_item(self, sku, name, category, tags, stock_status, available_stock):
        self.SKU = sku
        self.name = name
        self.category = category
        self.stock_status = stock_status
        self.available_stock = available_stock
        self.tags.set(tags)
        self.save()

    def delete_item(self):
        self.delete()
