# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
