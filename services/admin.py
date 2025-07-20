# services/admin.py
from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'branch', 'is_active', 'duration_minutes')
    list_filter = ('is_active', 'branch')
    search_fields = ('name', 'description')