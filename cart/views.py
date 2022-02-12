from django.views import generic
from .models import Product


class ProductListView(generic.ListView):
    template_name = 'cart/products.html'
    model = Product
    paginate_by = 3
