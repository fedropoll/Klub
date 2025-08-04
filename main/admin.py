from django.contrib import admin
from .models import CustomUser, UserProfile, ClientProfile, EmailVerificationCode
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Если уже регистрировали CustomUser где-то, то надо сначала отрегистировать
try:
    admin.site.unregister(CustomUser)
except admin.sites.NotRegistered:
    pass

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    # Не добавляем inline профили, чтобы не создавать дубликаты

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__email',)

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone')
    search_fields = ('user__email', 'full_name', 'phone')

@admin.register(EmailVerificationCode)
class EmailVerificationCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'created_at', 'is_used', 'is_expired']
    list_filter = ['is_used']
    search_fields = ['user__email', 'code']

    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Истек'
