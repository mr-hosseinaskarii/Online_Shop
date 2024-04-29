from django.contrib import admin
from .models import Product, Category, ProductImages


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImages)
