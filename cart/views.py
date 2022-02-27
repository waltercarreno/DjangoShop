from django.shortcuts import get_object_or_404, reverse, redirect
from django.views import generic
from .models import Product, OrderItem, Address
from django.contrib import messages
from django.shortcuts import render
from .utils import get_order_session
from .forms import AddToCartForm, Addressform
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


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

    def get_success_url(self):
        return reverse("cart:payment")

    def form_valid(self, form):
        "We have to validate our form and select our order session"
        order = get_order_session(self.request)
        selected_shipping_address = form.cleaned_data.get(
            'selected_shipping_address')
        selected_billing_address = form.cleaned_data.get(
            'selected_billing_address')

        if selected_shipping_address:
            order.shipping_address = selected_shipping_address
        else:
            address = Address.objects.create(
                address_type='S',
                user=self.request.user,
                address_line=form.cleaned_data['shipping_address_line'],
                zip_code=form.cleaned_data['shipping_zip_code'],
                city=form.cleaned_data['shipping_city'],
                country=form.cleaned_data['shipping_country'],
            )
            order.shipping_address = address

        if selected_billing_address:
            order.billing_address = selected_billing_address
        else:
            address = Address.objects.create(
                address_type='B',
                user=self.request.user,
                address_line=form.cleaned_data['billing_address_line'],
                zip_code=form.cleaned_data['billing_zip_code'],
                city=form.cleaned_data['billing_city'],
                country=form.cleaned_data['billing_country'],
            )
            order.billing_address = address

        order.save()
        messages.info(
            self.request, "You have successfully added your addresses")
        return super(CheckoutView, self).form_valid(form)

    "We have to parse our user id"
    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        return kwargs
    def get_context_data(self, **kwargs):
        """ We have to get the checkout and parse it the order"""
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context["order"] = get_order_session(self.request)
        return context
    
class PaymentView(generic.TemplateView):
    template_name = 'cart/payment.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        if not user.customer.stripe_customer_id:
            stripe_customer = stripe.Customer.create(email=user.email)
            user.customer.stripe_customer_id = stripe_customer["id"]
            user.customer.save()

            context = super(PaymentView, self).get_context_data(**kwargs)
            context["STRIPE_PUBLIC_KEY"] = settings.STRIPE_PUBLIC_KEY
            return context