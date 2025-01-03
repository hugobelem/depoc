from django.contrib import admin

from .models import Products, Category, CostHistory


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'unit', 'retailPrice', 'id')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


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


admin.site.register(Products, ProductsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CostHistory, CostHistoryAdmin)
