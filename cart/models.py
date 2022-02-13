from django.db import models
from django.shortcuts import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify

class Category(models.Model):
    """
    Category for products.
    """
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Define Products models.
    """
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=254)
    slug = models.SlugField(unique=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField()

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse("cart:product-detail", kwargs={'slug': self.slug})

    

def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(pre_save_product_receiver, sender=Product)
