from django.db import models


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
    sku = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField()

    def __str__(self):
        return self.name
