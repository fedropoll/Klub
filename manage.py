"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safe.settings')

    import django
    django.setup()

    from main.models import CustomUser

    # Создаем суперпользователя admin с ролью 'admin', если его нет
    try:
        user = CustomUser.objects.get(email="admin@gmail.com")
    except CustomUser.DoesNotExist:
        user = CustomUser.objects.create_superuser(
            email="admin@gmail.com",
            password="admin",
            username="admin"
        )
    if user.user_profile.role != 'admin':
        user.user_profile.role = 'admin'
        user.user_profile.save()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
