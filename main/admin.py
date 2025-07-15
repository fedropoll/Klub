from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# Если хочешь добавить UserProfile к User прямо в админке:
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserAdminWithProfile(UserAdmin):
    inlines = [UserProfileInline]

# Перерегистрируй User c новым админом:
admin.site.unregister(User)
admin.site.register(User, UserAdminWithProfile)

# Если хочешь отдельно:
# admin.site.register(UserProfile)
