from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# Настройки Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Safe Clinic API",
        default_version='v1',
        description="Полная документация API системы управления клиникой",
        terms_of_service="https://safeclinic.com/terms/",
        contact=openapi.Contact(email="api@safeclinic.com"),
        license=openapi.License(name="Commercial License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/branches/', include('branch.urls')),
    path('api/services/', include('services.urls')),
    path('api/doctors/', include('listdoctors.urls')),
    path('api/patients/', include('listpatients.urls')),
    path('api/appointments/', include('appointments.urls')),
    path('api/analytics/', include('data_analytics.urls')),
    path('api/auth/', include('main.urls')),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)