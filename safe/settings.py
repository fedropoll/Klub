import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import dj_database_url

# ----------------------------------------
# Пути
# ----------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Загружаем переменные окружения из .env (локально)
load_dotenv(BASE_DIR / ".env")

# ----------------------------------------
# Основные настройки
# ----------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# ALLOWED_HOSTS из переменных окружения (через запятую)
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# ----------------------------------------
# Порт для продакшена
# ----------------------------------------
PORT = int(os.environ.get("PORT", 8000))

# Доверенные источники для CSRF
CSRF_TRUSTED_ORIGINS = [f"https://{host.strip()}" for host in ALLOWED_HOSTS]

# Разрешаем все источники для CORS (можно ограничить при желании)
CORS_ALLOW_ALL_ORIGINS = True

# ----------------------------------------
# Безопасность
# ----------------------------------------
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ----------------------------------------
# Подключение к базе данных
# ----------------------------------------
DATABASES = {
    "default": dj_database_url.parse(
        os.getenv("DATABASE_URL") + "?sslmode=require"
    )
}

# ----------------------------------------
# JWT
# ----------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.getenv("ACCESS_TOKEN_LIFETIME", 60))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv("REFRESH_TOKEN_LIFETIME", 7))),
    "ROTATE_REFRESH_TOKENS": os.getenv("ROTATE_REFRESH_TOKENS", "True").lower() == "true",
    "BLACKLIST_AFTER_ROTATION": os.getenv("BLACKLIST_AFTER_ROTATION", "True").lower() == "true",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.RefreshToken",),
}

# ----------------------------------------
# Приложения
# ----------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "drf_yasg",
    "django_filters",

    "branch",
    "listdoctors",
    "listpatients",
    "services",
    "appointments",
    "main",
    "data_analytics",
]

# ----------------------------------------
# Middleware
# ----------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ----------------------------------------
# URLs и WSGI
# ----------------------------------------
ROOT_URLCONF = "safe.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "safe.wsgi.application"

# ----------------------------------------
# Статика и медиа
# ----------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ----------------------------------------
# REST Framework
# ----------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# ----------------------------------------
# Swagger
# ----------------------------------------
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Введите токен в формате: Bearer <your_token>",
        }
    },
    "USE_SESSION_AUTH": False,
}

# ----------------------------------------
# Пользовательская модель
# ----------------------------------------
AUTH_USER_MODEL = "main.CustomUser"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ----------------------------------------
# Email (если нужно)
# ----------------------------------------
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
