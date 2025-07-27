from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'full_name', 'phone', 'get_email', 'status'
    )
    search_fields = (
        'full_name', 'phone'
    )

    def get_email(self, obj):
        # Получаем email из связанного объекта User
        return obj.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__email'