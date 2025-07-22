from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import UserProfile, ClientProfile, Branch

# Отмена регистрации дефолтного User (если зарегистрирован)
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# Кастомный админ-сайт
class MyAdminSite(admin.AdminSite):
    site_header = "Панель Управления Клиникой Safe"
    site_title = "Админ Клиники Safe"
    index_title = "Добро пожаловать в панель управления"

my_admin_site = MyAdminSite(name='myadmin')

# Кастомный админ для User с дополнительным полем роли из UserProfile
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        "username", "email", "first_name", "last_name",
        "is_staff", "get_role"
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "userprofile__role")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)
    filter_horizontal = ("groups", "user_permissions")

    def get_role(self, obj):
        try:
            return obj.userprofile.get_role_display()
        except UserProfile.DoesNotExist:
            return _("Нет роли")
    get_role.short_description = _("Роль")

# Регистрация моделей UserProfile, ClientProfile, Branch в админку
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    search_fields = ("user__username", "role")
    list_filter = ("role",)

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "is_email_verified")
    search_fields = ("user__username", "full_name")

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "director", "is_active", "phone_number", "email")
    search_fields = ("name", "address", "director__username")
    list_filter = ("is_active",)

# Зарегистрировать кастомный UserAdmin на нашем кастомном сайте
my_admin_site.register(User, CustomUserAdmin)
my_admin_site.register(UserProfile, UserProfileAdmin)
my_admin_site.register(ClientProfile, ClientProfileAdmin)
my_admin_site.register(Branch, BranchAdmin)
