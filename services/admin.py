# services/admin.py
from django.contrib import admin
from .models import Service, Category

# Регистрируем модель Service в админ-панели
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_minutes', 'is_active', 'branch', 'category', 'created_at')
    list_filter = ('is_active', 'branch', 'category')
    search_fields = ('name', 'description')
    raw_id_fields = ('branch', 'category') # Полезно для выбора связанных объектов
    date_hierarchy = 'created_at'

# Регистрируем модель Category в админ-панели
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)