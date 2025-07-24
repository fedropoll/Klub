from django.contrib import admin
from django.utils.html import mark_safe
from .models import Branch

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'phone', 'director')  # столбцы в списке
    search_fields = ('name', 'address', 'phone', 'director__username')  # поиск по этим полям
    list_filter = ('director',)  # фильтры сбоку

    readonly_fields = ('photo_preview',)

    def photo_preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100" height="100" />')
        return "-"
    photo_preview.short_description = 'Photo Preview'
