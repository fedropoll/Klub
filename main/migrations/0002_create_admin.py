# safe_clinic/migrations/0002_create_admin.py
from django.db import migrations
from django.contrib.auth import get_user_model

def create_admin(apps, schema_editor):
    User = get_user_model()
    if not User.objects.filter(email="admin@gmail.com").exists():
        User.objects.create_superuser(email="admin@gmail.com", password="admin123")

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0001_initial'),  # замените на вашу первую миграцию
    ]
    operations = [
        migrations.RunPython(create_admin),
    ]
