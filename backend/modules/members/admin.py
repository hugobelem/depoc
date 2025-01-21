from django.contrib import admin
from django.contrib.admin import register

from .models import Member


@register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'cpf', 'salary', 'has_access', 'is_active']
