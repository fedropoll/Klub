from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Swagger / drf-yasg
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Импорты ваших views
from main.admin import my_admin_site
from main.views import (
    RegisterAPIView,
    ClientRegisterAPIView,
    VerifyEmailAPIView,
    ResendVerifyCodeAPIView,
)

# Swagger schema
schema_view = get_schema_view(
    openapi.Info(
        title="Safe Clinic API",
        default_version='v1',
        description="Документация API для управления клиникой",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourclinic.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# URL-шки
urlpatterns = [
    path('admin/', my_admin_site.urls),

    # Регистрация
    path('api/register/', RegisterAPIView.as_view(), name='register-staff'),
    path('api/register/client/', ClientRegisterAPIView.as_view(), name='register-client'),
    path('api/verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('api/resend-verify-code/', ResendVerifyCodeAPIView.as_view(), name='resend-verify-code'),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Доктора
    path('api/list_doctor/', include('listdoctors.urls')),
    path('api/list_patients', include('listpatients.urls')),
    # Swagger и ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
