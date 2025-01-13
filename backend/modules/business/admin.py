from django.contrib import admin
from django.contrib.admin import register

from .models import Business


@register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['legal_name', 'trade_name', 'registration_number', 'is_active']
