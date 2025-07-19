from django.contrib import admin
from django.contrib.auth.models import User
from .models import Branch

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'get_director_email', 'phone_number')
    search_fields = ('name', 'address', 'director__email', 'phone_number')
    list_filter = ('director',)
    fieldsets = (
        (None, {'fields': ('name', 'address', 'phone_number')}),
        ('Руководство', {'fields': ('director',)}),
    )

    def get_director_email(self, obj):
        return obj.director.email if obj.director else None
    get_director_email.short_description = 'Директор (Email)'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "director":
            # Убрана фильтрация по is_staff=True, теперь отображаются все пользователи
            pass # Нет специфичной фильтрации, используются все объекты User
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
