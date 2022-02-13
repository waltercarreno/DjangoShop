from django.views import generic
from .models import Product
from django.contrib import messages
from django.shortcuts import render

class ProductListView(generic.ListView):
    template_name = 'cart/products.html'
    model = Product
    paginate_by = 3
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(name__icontains=query)
        else: 
            object_list = self.model.objects.all()
        return object_list

class ProductDetailView(generic.DetailView):
    template_name = 'cart/productdetail.html'
    queryset = Product.objects.all()