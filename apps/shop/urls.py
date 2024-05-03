from django.urls import path
from .views import IndexView, ProductDetailView

app_name = 'shop'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path("products/<int:pk>", ProductDetailView.as_view(), name='product-detail'),
]
