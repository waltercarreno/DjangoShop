from django.shortcuts import get_object_or_404, reverse, redirect
from django.views import generic
from .models import Product, OrderItem
from django.contrib import messages
from django.shortcuts import render
from .utils import get_order_session
from .forms import AddToCartForm, Addressform


class ProductListView(generic.ListView):
    """A View that  contents products and pagination."""
    template_name = 'cart/products.html'
    model = Product
    paginate_by = 3
    """Used to filter throw the data"""
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(name__icontains=query)
        else:
            object_list = self.model.objects.all()
        return object_list


class ProductDetailView(generic.FormView):
    template_name = 'cart/product_detail.html'
    """ We have to pick forms from forms.py"""
    form_class = AddToCartForm

    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs["slug"])

    def get_success_url(self):
        return reverse("home")

    def form_valid(self, form):
        order = get_order_session(self.request)
        product = self.get_object()
        item_filter = order.items.filter(product=product)

        if item_filter.exists():
            item = item_filter.first()
            item.quantity = int(form.cleaned_data['quantity'])
            item.save()
        else:
            new_item = form.save(commit=False)
            new_item.product = product
            new_item.order = order
            new_item.save()

        return super(ProductDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['product'] = self.get_object()
        return context


class BagView(generic.TemplateView):
    template_name = "cart/bag.html"
    """ We have to get the bag and parse it the order"""
    def get_context_data(self, **kwargs):
        context = super(BagView, self).get_context_data(**kwargs)
        context["order"] = get_order_session(self.request)
        return context


class IncreaseProductView(generic.View):
    """ We have to get the item in the order to be able to modify quantity"""
    def get(self, request, *args, **kwargs):
        del request, args
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.quantity += 1
        order_item.save()
        return redirect("cart:bag")


class DecreaseProductView(generic.View):
    """ We have to get the item in the order to be able to modify quantity"""
    def get(self, request, *args, **kwargs):
        del args, request
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        if order_item.quantity <= 1:
            order_item.delete()
        else:
            order_item.quantity -= 1
            order_item.save()
        return redirect("cart:bag")


class RemoveProductView(generic.View):
    """ We have to get the item in the order to be able to modify quantity"""
    def get(self, request, *args, **kwargs):
        del request, args
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.delete()
        return redirect("cart:bag")


class CheckoutView(generic.FormView):
    template_name = "cart/checkout.html"
    form_class = Addressform