from django.contrib import admin

from modules.business.models import Business, BusinessOwner


class BusinessAdmin(admin.ModelAdmin):
    list_display = ('id', 'tradeName', 'registrationNumber')

class BusinessOwnerAdmin(admin.ModelAdmin):
    list_display = ('owner', 'business')


admin.site.register(Business, BusinessAdmin)
admin.site.register(BusinessOwner, BusinessOwnerAdmin)
