from django.contrib import admin
from django.contrib.admin import register

from .forms import CustomUserCreationForm, CustomUserChangeForm

from .models import User, Owner


@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'email', 'is_superuser', 'is_active', 'id']
    readonly_fields = ['last_login', 'date_joined']

    def get_fields(self, request, obj=None):
        common_fields = [
            'name',
            'email',
            'username',
            'is_active',
            'is_staff',
            'is_superuser',
        ]

        if obj is None:
            return common_fields + ['password1', 'password2']
        else:
            return common_fields + ['last_login', 'date_joined', 'groups']
        

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            form_class = CustomUserCreationForm
        else:
            form_class = CustomUserChangeForm

        kwargs['form'] = form_class
        return super().get_form(request, obj, **kwargs)


@register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['user', 'business', 'name', 'email', 'phone']
