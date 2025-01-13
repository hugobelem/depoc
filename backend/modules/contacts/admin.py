from django.contrib import admin
from django.contrib.admin import register

from .models import Customer, Supplier


@register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'alias', 'cpf', 'business']
    readonly_fields = ['amount_spent', 'number_of_orders']


@register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['code', 'legal_name', 'trade_name', 'cnpj', 'business']
