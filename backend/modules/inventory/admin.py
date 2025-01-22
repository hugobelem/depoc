from django.contrib import admin
from django.contrib.admin import register

from .models import Inventory, InventoryTransaction


@register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity']


@register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'inventory',
        'type',
        'date',
        'quantity',
        'unit_cost',
        'unit_price',
        'description',
    ]
