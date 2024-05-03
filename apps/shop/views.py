from django.views import generic
from apps.shop.models import Product
from django.shortcuts import render


class IndexView(generic.ListView):
    model = Product
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_products'] = Product.objects.all()[:5]
        return context


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'shop/product-detail.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        product = Product.objects.get(id=pk)
        return render(request, self.template_name, {'product': product})
