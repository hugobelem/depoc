from django.contrib import admin
from django.contrib.admin import register

from .models import Product, ProductCategory, ProductCostHistory


@register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'retail_price', 'stock', 'unit', 'is_available']


@register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'business', 'is_active']


@register(ProductCostHistory)
class ProductCostHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'quantity',
        'effective_date',
        'cost_price',
        'average_cost',
        'retail_price',
        'markup',
    ]
