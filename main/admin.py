# /home/asylbek/Desktop/klub/safe/main/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserProfile, ClientProfile, Branch

admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'get_full_name', # Метод для получения полного имени
        'get_role',
        'is_active',
        'is_staff',
        'date_joined',
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'userprofile__role')

    def get_role(self, obj):
        try:
            return obj.userprofile.get_role_display()
        except UserProfile.DoesNotExist:
            return "Нет роли"
    get_role.short_description = 'Роль'

    # ДОБАВЬТЕ ЭТОТ МЕТОД, чтобы переименовать столбец 'Get full name'
    def get_full_name(self, obj):
        return obj.get_full_name() # Вызываем оригинальный метод User.get_full_name
    get_full_name.short_description = 'Полное имя' # Название столбца

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'role')
    list_filter = ('role',)

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'is_email_verified')
    search_fields = ('user__username', 'full_name')

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'director', 'is_active', 'phone_number', 'email')
    search_fields = ('name', 'address', 'director__username')
    list_filter = ('is_active',)

