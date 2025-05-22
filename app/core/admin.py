# Django admin cusomization

from django.contrib import admin  # type: ignore
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin  # type: ignore
from django.utils.translation import gettext_lazy as _  # type: ignore

from core import models  # type: ignore


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['username', 'email', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone', 'cuit', 'specialization')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

admin.site.register(models.CustomUser, UserAdmin)