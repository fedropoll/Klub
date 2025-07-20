from django.contrib import admin
from .models import Branch, Service

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'get_director_email', 'phone_number', 'photo')
    search_fields = ('name', 'address', 'director__email', 'phone_number')
    list_filter = ('director',)

    def get_director_email(self, obj):
        return obj.director.email if obj.director else None
    get_director_email.short_description = 'Директор (Email)'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'branch', 'is_active', 'duration_minutes')
    list_filter = ('is_active', 'branch')
    search_fields = ('name', 'description')