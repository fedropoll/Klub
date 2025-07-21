from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

# Попытка отрегать дефолтный User (на всякий случай)
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

# Объединённый админ-класс для пользователей
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "get_user_group")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)
    filter_horizontal = ("groups", "user_permissions")

    def get_user_group(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_user_group.short_description = _("Группы")

# Зарегистрировать User с кастомным админом на нашем сайте
my_admin_site.register(User, CustomUserAdmin)

