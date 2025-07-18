from django.contrib import admin
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