"""
All models.
"""
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.shortcuts import reverse
from django.utils.text import slugify


User = get_user_model()


class Address(models.Model):
    """
    Address for shipment need for checkout.
    """
    ADDRESS_CHOICES = (
        ('B', 'Billing'),
        ('S', 'Shipping'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address_line_1}, {self.address_line_2},\
        {self.city}, {self.zip_code}"

    class Meta:
        """Fixing typing error"""
        verbose_name_plural = 'Addresses'


class Category(models.Model):
    """
    Category for products.
    """
    name = models.CharField(max_length=254)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    """
    Define Products models.
    """
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=254)
    slug = models.SlugField(unique=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2,
                                 null=True, blank=True)
    image = models.ImageField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        """Redirect to product template.Slug to identify item"""
        return reverse("cart:product-detail", kwargs={'slug': self.slug})

    def get_price(self):
        """To get 2 decimal numbers"""
        return str(self.price)


class OrderItem(models.Model):
    """
    Order created. We select quantity. Necessary for bag "
    """
    order = models.ForeignKey(
        "Order", related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get__item_price(self):
        """We get quantity and multiply * price"""
        return self.quantity * self.product.price

    def get_total_item_price(self):
        """We use the previous function to calculate the total price"""
        price = self.get__item_price()
        return price


class Order(models.Model):
    """
    Order created. Checkout and payment"
    """
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(Address, related_name='billing_post',
                                        blank=True, null=True,
                                        on_delete=models.SET_NULL)
    shipping_address = models.ForeignKey(Address,
                                         related_name='shipping_address',
                                         blank=True,
                                         null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.reference_number

    @property
    def reference_number(self):
        """We take our primary key in select our order"""
        return f"ORDER-{self.pk}"

    def get_raw_subtotal(self):
        """We Calculate the number of items in our bag and the price"""
        total = 0
        for order_item in self.items.all():
            total += order_item.get__item_price()
        return total

    def get_subtotal(self):
        """We calculate our subtotal"""
        subtotal = self.get_raw_subtotal()
        return subtotal

    def get_raw_total(self):
        """We calculate our total and delivery cost"""
        subtotal = self.get_raw_subtotal()
        delivery = 5
        if subtotal > 50:
            total = subtotal
        else:
            total = subtotal + delivery
        return total

    def get_total(self):
        """We get our total cost """
        total = self.get_raw_total()
        return total


def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(pre_save_product_receiver, sender=Product)
