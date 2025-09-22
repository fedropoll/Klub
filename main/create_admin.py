# safe_clinic/create_admin.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "safe.settings")
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

EMAIL = "admin@gmail.com"
PASSWORD = "admin"  # ставь свой пароль

if not User.objects.filter(email=EMAIL).exists():
    User.objects.create_superuser(email=EMAIL, password=PASSWORD)
    print(f"✅ Новый суперюзер создан: {EMAIL}")
else:
    print(f"Суперюзер {EMAIL} уже существует")
