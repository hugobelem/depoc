from django.contrib import admin
from django.contrib.admin import register

from .models import (
    Animal,
    AnimalFinancial,
    AnimalLifeCycle,
    AnimalGrowth,
    AnimalWeight,
    AnimalMeatQuality,
    AnimalHealth,
)

@register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['tagNumber', 'species', 'status', 'id']

