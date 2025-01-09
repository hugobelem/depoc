from django.contrib import admin
from django.contrib.admin import register

from .models import Transaction


@register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['type', 'amount', 'description', 'timestamp', 'bankAccount']
