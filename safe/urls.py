from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from main.views import (
    RegisterAPIView,
    ClientRegisterAPIView,
    VerifyEmailAPIView,
    ResendVerifyCodeAPIView,
)

# УДАЛЯЕМ импорт нашего кастомного AdminSite
# from main.admin import my_admin_site

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

urlpatterns = [
    # Возвращаем стандартный admin.site.urls
    path('admin/', admin.site.urls),

    # Сотрудники (Регистрация сотрудников)
    path('api/register/', RegisterAPIView.as_view(), name='register-staff'),

    # Клиенты (Регистрация клиентов и подтверждение email)
    path('api/register/client/', ClientRegisterAPIView.as_view(), name='register-client'),
    path('api/verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('api/resend-verify-code/', ResendVerifyCodeAPIView.as_view(), name='resend-verify-code'),

    # JWT Аутентификация
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API для управления филиалами (перемещено в list_doctor)
    path('api/list_doctor/', include('list_doctor.urls')),

    # Swagger и Redoc документация
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]