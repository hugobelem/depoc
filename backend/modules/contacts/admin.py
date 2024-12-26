from django.contrib import admin

from .models import Contacts


class ContactsAdmin(admin.ModelAdmin):
    list_display = ('name', 'alias', 'code', 'entityId')


admin.site.register(Contacts, ContactsAdmin)
