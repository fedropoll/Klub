# main/admin.py
from django.contrib import admin
from django.contrib.auth.models import User
# ... другие импорты ...

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

class MyAdminSite(admin.AdminSite):
    site_header = "Панель Управления Клиникой Safe"
    site_title = "Админ Клиники Safe"
    index_title = "Добро пожаловать в панель управления"

# Создаем экземпляр нашего кастомного сайта
my_admin_site = MyAdminSite(name='myadmin')

# --- Регистрируем ВСЕ МОДЕЛИ на кастомном сайте ---
my_admin_site.register(User, StaffUserAdmin)
my_admin_site.register(User, ClientUserAdmin)
# ... другие регистрации моделей ...

# Импортируем Branch и BranchAdmin и регистрируем ИХ ЗДЕСЬ
from list_doctor.models import Branch
from list_doctor.admin import BranchAdmin

my_admin_site.register(Branch, BranchAdmin) # <--- Регистрация происходит только здесь