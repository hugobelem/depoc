from django.contrib import admin
from django.contrib.admin import register

from .models import FinancialAccount, FinancialCategory, FinancialTransaction


@register(FinancialAccount)
class FinancialAccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'balance', 'business', 'is_active']
    readonly_fields = ['balance']


@register(FinancialCategory)
class FinancialCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'business', 'is_active']


@register(FinancialTransaction)
class FinancialTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'description',
        'amount',
        'type',
        'account',
        'timestamp',
        'category',
    ]
