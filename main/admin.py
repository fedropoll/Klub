<<<<<<< HEAD
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
        'get_full_name',
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
=======
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
>>>>>>> aziret

