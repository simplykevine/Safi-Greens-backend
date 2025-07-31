from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ('phone_number', 'name', 'user_type', 'is_active', 'is_staff')
    ordering = ('phone_number',)
    search_fields = ('phone_number', 'name')
    fieldsets = (
        (None, {'fields': ('phone_number', 'name', 'password', 'user_type')}),
        ('Personal info', {'fields': ('profile_picture', 'location', 'shop_name', 'till_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'name', 'user_type', 'password1', 'password2')}
        ),
    )

admin.site.register(User, CustomUserAdmin)