from django.contrib import admin

from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'email')
    readonly_fields = ['last_login', 'date_joined']

    def get_fields(self, request, obj=None):
        if obj is None:
            self.fields = [
                'name',
                'email',
                'username',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',           
            ]
        else:
            self.fields = [
                'name',
                'email',
                'username',
                'is_active',
                'is_staff',
                'is_superuser',
                'last_login',
                'date_joined',
                'groups',                
            ]
        return super().get_fields(request, obj)
    
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            self.form = CustomUserCreationForm
        else:
            self.form = CustomUserChangeForm
        return super().get_form(request, obj, **kwargs)
    

admin.site.register(User, UserAdmin)
