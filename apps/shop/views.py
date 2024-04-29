from django.views import generic
from apps.shop.models import Product


class IndexView(generic.ListView):
    model = Product
    template_name = 'shop/index.html'
