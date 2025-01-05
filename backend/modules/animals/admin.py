from django.contrib import admin

from .models import Animals


class AnimalsAdmin(admin.ModelAdmin):
    list_display = ['species', 'breed', 'gender', 'arrivalDate', 'weight']


admin.site.register(Animals, AnimalsAdmin)
