from django.contrib import admin
from .models import Product, Category, Order, OrderItem

# Register your models here.

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