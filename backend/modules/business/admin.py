from django.contrib import admin

from modules.business.models import Business, BusinessOwner, BusinessMembers


class BusinessAdmin(admin.ModelAdmin):
    list_display = ('id', 'tradeName', 'registrationNumber')

class BusinessOwnerAdmin(admin.ModelAdmin):
    list_display = ('owner', 'business')

class BusinessMembersAdmin(admin.ModelAdmin):
    list_display = ('members', 'business')


admin.site.register(Business, BusinessAdmin)
admin.site.register(BusinessOwner, BusinessOwnerAdmin)
admin.site.register(BusinessMembers, BusinessMembersAdmin)
