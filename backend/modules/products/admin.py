from django.contrib import admin

from .models import Products, Category, CostHistory, ProductSource


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'retailPrice')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class CostHistoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'quatity', 'effectiveDate', 'costPrice']


admin.site.register(Products, ProductsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CostHistory, CostHistoryAdmin)
