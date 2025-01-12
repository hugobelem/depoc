# from django.contrib import admin
# from django.contrib.admin import register

# from .models import (
#     Animal,
#     AnimalFinancial,
#     AnimalLifeCycle,
#     AnimalGrowth,
#     AnimalWeight,
#     AnimalMeatQuality,
#     AnimalHealth,
# )

# @register(Animal)
# class AnimalAdmin(admin.ModelAdmin):
#     list_display = ['tagNumber', 'species', 'status', 'id']

# @register(AnimalFinancial)
# class AnimalFinancialAdmin(admin.ModelAdmin):
#     list_display = ['animal', 'purchaseCost', 'maintenanceCost', 'estimatedValue']

# @register(AnimalLifeCycle)
# class AnimalLifeCycleAdmin(admin.ModelAdmin):
#     list_display = ['animal', 'arrivalDate', 'processedDate']

# @register(AnimalGrowth)
# class AnimalGrowthAdmin(admin.ModelAdmin):
#     list_display = ['animal', 'feedType', 'feedConsumed', 'GrowthRate']

# @register(AnimalWeight)
# class AnimalWeightAdmin(admin.ModelAdmin):
#     list_display = [
#         'animal',
#         'weight',
#         'processedWeight',
#         'carcassWeight',
#         'dressingPercentage',
#     ]

# @register(AnimalMeatQuality)
# class AnimalMeatQualityAdmin(admin.ModelAdmin):
#     list_display = ['animal', 'backFatThickness']

# @register(AnimalHealth)
# class AnimalHealthAdmin(admin.ModelAdmin):
#     list_display = ['animal', 'healthStatus', 'notes']
