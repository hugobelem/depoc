from django.contrib import admin

from .models import Members, MembersCredentials


class MembersAdmin(admin.ModelAdmin):
    list_display = ['id', 'firstName', 'role', 'status']

class MembersCredentialsAdmin(admin.ModelAdmin):
    list_display = ['member', 'credentials']


admin.site.register(Members, MembersAdmin)
admin.site.register(MembersCredentials, MembersCredentialsAdmin)
