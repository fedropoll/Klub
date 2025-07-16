from django import forms
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import UserProfile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_full_name', 'is_staff')

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
    get_full_name.short_description = 'ФИО'

# Перерегистрируем User с новым админом
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Inline для UserProfile (показывает роль и другую инфу рядом с User)
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль пользователя'

class UserChangeForm(forms.ModelForm):
    full_name = forms.CharField(label='ФИО', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name',
                  'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',
                  'last_login', 'date_joined', 'full_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['full_name'].initial = f"{self.instance.first_name} {self.instance.last_name}".strip()
            self.fields['username'].widget.attrs['readonly'] = True

    def clean_username(self):
        return self.instance.username

    def save(self, commit=True):
        full_name = self.cleaned_data.get('full_name', '')
        parts = full_name.split(' ', 1)
        self.instance.first_name = parts[0] if len(parts) > 0 else ''
        self.instance.last_name = parts[1] if len(parts) > 1 else ''
        return super().save(commit)

class CustomUserAdmin(DefaultUserAdmin):
    inlines = (UserProfileInline,)

    list_display = ('email', 'full_name_display', 'get_role', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'userprofile__role')

    form = UserChangeForm

    def full_name_display(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
    full_name_display.short_description = 'ФИО'

    def get_role(self, obj):
        return obj.userprofile.role if hasattr(obj, 'userprofile') else ''
    get_role.short_description = 'Роль'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
