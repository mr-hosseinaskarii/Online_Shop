from django.db import models
from apps.shop.models import Product
from apps.account.models import CustomUser


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=3)


STATUS_CHOICE = (
    ('Pending', 'pending'),
    ('Processing', 'processing'),
    ('Sending', 'sending'),
    ('Delivered', 'delivered'),
    ('Completed', 'completed'),
)


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=3)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default='Pending')
