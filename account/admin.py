from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models.user_model import User
from .models.role_model import Role


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'phone', 'is_staff', 'is_superuser', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
        ('Roles', {'fields': ('roles',)}),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'created_at')
    list_filter = ('level', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    ordering = ('level',)
