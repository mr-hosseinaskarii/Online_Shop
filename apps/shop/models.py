from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name


class ProductImages(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    images = models.ImageField(upload_to='products/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "product images"

    def __str__(self):
        return f"Image for {self.product.name}"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    amount = models.IntegerField()
    discount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    max_discount_amount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    min_discount_amount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def discounted_price(self):
        discount_amount = min(self.price, self.max_discount_amount)
        discounted_price = self.price - discount_amount
        discounted_price -= discounted_price * (self.discount / 100)
        return discounted_price
