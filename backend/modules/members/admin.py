from django.contrib import admin

from .models import Members


class MembersAdmin(admin.ModelAdmin):
    list_display = ['id', 'firstName', 'role', 'status']


admin.site.register(Members, MembersAdmin)
