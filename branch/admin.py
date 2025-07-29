from django.contrib import admin
from .models import Branch

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'phone', 'director')
    search_fields = ('name', 'address', 'phone', 'director__email') # Изменено на director__email
    list_filter = ('director',)
