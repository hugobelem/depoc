from django.contrib import admin

from .models import Members, MembersCredentials


class MembersAdmin(admin.ModelAdmin):
    list_display = ['id', 'taxId', 'email', 'role', 'status']

class MembersCredentialsAdmin(admin.ModelAdmin):
    list_display = ['member', 'credential']


admin.site.register(Members, MembersAdmin)
admin.site.register(MembersCredentials, MembersCredentialsAdmin)
