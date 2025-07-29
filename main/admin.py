from django.contrib import admin
from .models import UserProfile, ClientProfile, EmailVerificationCode, CustomUser # Добавлен CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

try:
    admin.site.unregister(CustomUser) # Изменено на CustomUser
except admin.sites.NotRegistered:
    pass

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль пользователя'
    fk_name = 'user'

class ClientProfileInline(admin.StackedInline):
    model = ClientProfile
    can_delete = False
    verbose_name_plural = 'Профиль клиента'
    fk_name = 'user'
    fields = (
    'full_name', 'phone', 'birth_date', 'gender', 'address', 'about', 'is_email_verified', 'confirmation_code',
    'code_created_at')
    readonly_fields = ('confirmation_code', 'code_created_at', 'is_email_verified')

@admin.register(CustomUser) # Изменено на CustomUser
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

    list_display = ('email', 'first_name', 'last_name', 'is_active', 'get_role', 'get_full_name', 'get_is_email_verified') # Изменено для отображения email
    list_filter = BaseUserAdmin.list_filter + (
    'user_profile__role',)

    search_fields = (
    'email', 'first_name', 'last_name', 'client_profile__full_name', 'client_profile__phone') # Убрано username

    def get_role(self, obj):
        return obj.user_profile.get_role_display() if hasattr(obj, 'user_profile') else 'N/A'

    get_role.short_description = 'Роль'
    get_role.admin_order_field = 'user_profile__role'

    def get_full_name(self, obj):
        return obj.client_profile.full_name if hasattr(obj, 'client_profile') and obj.client_profile else 'N/A'

    get_full_name.short_description = 'Полное имя клиента'

    def get_is_email_verified(self, obj):
        return obj.client_profile.is_email_verified if hasattr(obj, 'client_profile') and obj.client_profile else False

    get_is_email_verified.short_description = 'Email подтвержден'
    get_is_email_verified.boolean = True


@admin.register(EmailVerificationCode)
class EmailVerificationCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'created_at', 'is_used', 'is_expired']
    list_filter = ['is_used']
    search_fields = ['user__email', 'code']

    def is_expired(self, obj):
        return obj.is_expired()

    is_expired.boolean = True
    is_expired.short_description = 'Истек'
