# main/migrations/000X_create_admin_user.py
from django.db import migrations

def create_admin(apps, schema_editor):
    CustomUser = apps.get_model("main", "CustomUser")
    UserProfile = apps.get_model("main", "UserProfile")

    if not CustomUser.objects.filter(email="admin@gmail.com").exists():
        user = CustomUser.objects.create_superuser(
            email="admin@gmail.com",
            username="admin",
            password="admin"
        )
        profile = UserProfile.objects.get(user=user)
        profile.role = "admin"
        profile.save()

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),  # последняя существующая миграция у тебя 0001_initial
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]
