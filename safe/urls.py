from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from main.views import (
    MyTokenObtainPairView,
    AdminTokenObtainPairView,
    DoctorTokenObtainPairView,
    DirectorTokenObtainPairView
)


schema_view = get_schema_view(
    openapi.Info(
        title="API Клиники Safe v1",
        default_version='v1',
        description="Документация по API.",
        contact=openapi.Contact(email="contact@safe.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('services/', include('services.urls')),
    path('list_doctor/', include('listdoctors.urls')),
    path('list_patients/', include('listpatients.urls')),
    path('branches/', include('branch.urls')),
    path('appointments/', include('appointments.urls')),
    path('analytics/', include('data_analytics.urls')), # <-- ДОБАВЛЕНО

    path('', include('main.urls')),
    path('api/token/client', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/admin/', AdminTokenObtainPairView.as_view(), name='token_admin'),
    path('api/token/doctor/', DoctorTokenObtainPairView.as_view(), name='token_doctor'),
    path('api/token/director/', DirectorTokenObtainPairView.as_view(), name='token_director'),


    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)