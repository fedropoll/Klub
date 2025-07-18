# main/admin.py
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, ClientProfile, ClientManager, StaffManager


# --- Базовая форма для User, включает ФИО ---
class BaseUserChangeForm(forms.ModelForm):
    full_name = forms.CharField(label='ФИО', required=False, help_text='Имя и Фамилия пользователя.')

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.first_name and self.instance.last_name:
            self.fields['full_name'].initial = f"{self.instance.first_name} {self.instance.last_name}".strip()
        self.fields['first_name'].widget = forms.HiddenInput()
        self.fields['last_name'].widget = forms.HiddenInput()
        self.fields['username'].widget = forms.HiddenInput() # Скрываем username, т.к. используем email

    def clean_username(self):
        if self.instance and self.instance.email:
            return self.instance.email
        return self.cleaned_data.get('email')

    def save(self, commit=True):
        full_name = self.cleaned_data.get('full_name', '')
        parts = full_name.split(' ', 1)
        self.instance.first_name = parts[0] if len(parts) > 0 else ''
        self.instance.last_name = parts[1] if len(parts) > 1 else ''
        return super().save(commit)

# --- Инлайн для UserProfile ---
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль пользователя'

# --- Инлайн для ClientProfile ---
class ClientProfileInline(admin.StackedInline):
    model = ClientProfile
    can_delete = False
    verbose_name_plural = 'Профиль клиента'
    readonly_fields = ('confirmation_code', 'code_created_at')

# --- Сотрудники (Staff) Админ ---
# Обратите внимание: User регистрируется дважды в этом файле, что приведет к AlreadyRegistered
# Но мы возвращаем к исходному состоянию по запросу.
class StaffUserAdmin(DefaultUserAdmin):
    inlines = (UserProfileInline,)
    form = BaseUserChangeForm

    def get_queryset(self, request):
        return StaffManager().get_queryset()

    list_display = ('email', 'full_name_display', 'get_role', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'userprofile__role')
    list_filter = ('is_staff', 'is_active', 'userprofile__role')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('full_name', 'email')}),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    def full_name_display(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
    full_name_display.short_description = 'ФИО'

    def get_role(self, obj):
        return obj.userprofile.get_role_display() if hasattr(obj, 'userprofile') else ''
    get_role.short_description = 'Роль'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change and not hasattr(obj, 'userprofile'):
            UserProfile.objects.create(user=obj, role='doctor')
        if hasattr(obj, 'userprofile') and obj.userprofile.role == 'patient':
            obj.userprofile.role = 'doctor'
            obj.userprofile.save()

admin.site.register(User, StaffUserAdmin) # Первая регистрация User

# --- Клиенты (Clients) Админ ---
class ClientUserAdmin(DefaultUserAdmin):
    inlines = (ClientProfileInline, UserProfileInline)
    form = BaseUserChangeForm

    def get_queryset(self, request):
        return ClientManager().get_queryset()

    list_display = ('email', 'full_name_display', 'get_is_email_verified', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'clientprofile__full_name')
    list_filter = ('is_active', 'clientprofile__is_email_verified')
    ordering = ('email',)

    # ЭТОТ БЛОК fieldsets вызовет TypeError: 'tuple' object does not support item assignment
    # так как fieldsets был кортежем, а не списком, но мы возвращаем его как было.
    fieldsets = DefaultUserAdmin.fieldsets
    fieldsets[2] = ('Статус', {'fields': ('is_active',)}) # Переопределяем секцию прав доступа, чтобы оставить только is_active
    # fieldsets[2] здесь будет ссылаться на immutable tuple

    def full_name_display(self, obj):
        return obj.clientprofile.full_name if hasattr(obj, 'clientprofile') else f"{obj.first_name} {obj.last_name}".strip()
    full_name_display.short_description = 'ФИО Клиента'

    def get_is_email_verified(self, obj):
        return obj.clientprofile.is_email_verified if hasattr(obj, 'clientprofile') else False
    get_is_email_verified.boolean = True
    get_is_email_verified.short_description = 'Email подтвержден'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change and not hasattr(obj, 'userprofile'):
            UserProfile.objects.create(user=obj, role='patient')
        elif hasattr(obj, 'userprofile') and obj.userprofile.role != 'patient':
            obj.userprofile.role = 'patient'
            obj.userprofile.save()
        if not change and not hasattr(obj, 'clientprofile'):
            ClientProfile.objects.create(
                user=obj,
                full_name=form.cleaned_data.get('full_name', ''),
                confirmation_code='0000',
                is_email_verified=True
            )

admin.site.register(User, ClientUserAdmin) # Вторая регистрация User - вызовет AlreadyRegistered

# Удаляем MyAdminSite и все связанные с ним строки регистрации
# class MyAdminSite(admin.AdminSite):
#     site_header = "Панель Управления Клиникой Safe"
#     site_title = "Админ Клиники Safe"
#     index_title = "Добро пожаловать в панель управления"
# my_admin_site = MyAdminSite(name='myadmin')
# my_admin_site.register(User, StaffUserAdmin)
# my_admin_site.register(User, ClientUserAdmin)
# my_admin_site.register(UserProfile)
# my_admin_site.register(ClientProfile)
# from list_doctor.models import Branch
# from list_doctor.admin import BranchAdmin
# my_admin_site.register(Branch, BranchAdmin)