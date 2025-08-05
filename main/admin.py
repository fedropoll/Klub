from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, ClientProfile, EmailVerificationCode

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль пользователя'
    fk_name = 'user'

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    list_display = ('email', 'is_staff', 'is_active', 'get_role')
    list_select_related = ('user_profile',)
    ordering = ('email',)
    search_fields = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'username', 'is_staff', 'is_active')}
        ),
    )

    def get_role(self, obj):
        return obj.user_profile.role if hasattr(obj, 'user_profile') else '—'
    get_role.short_description = 'Роль'
    get_role.admin_order_field = 'user_profile__role'


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
