from django.contrib import admin
from .models import Product, Category, Order, OrderItem
"""
registration admin for products, order and category.
"""


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'slug',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('slug',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)

