from django.contrib import admin
from django.contrib.admin import register

from .models import Products, Category, CostHistory, ProductAnimal

@register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'unit', 'retailPrice', 'id']

@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@register(CostHistory)
class CostHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'quantity',
        'effectiveDate',
        'costPrice',
        'costAverage',
        'retailPrice',
        'markup',
    ]

@register(ProductAnimal)
class ProductAnimalAdmin(admin.ModelAdmin):
    list_display = ['animal', 'product', 'packagingDate', 'expirationDate']
