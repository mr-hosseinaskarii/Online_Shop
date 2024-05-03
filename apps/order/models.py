from django.db import models
from apps.shop.models import Product
from apps.accounts.models import CustomUser
from django.core.validators import MinValueValidator


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


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

    @property
    def get_order_total(self):
        order_items = self.order_items.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.order_items.all()
        total = sum([item.quantity for item in order_items])
        return total


class Discount(models.Model):
    code = models.CharField(max_length=50, unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='discount')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='discount')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.code
