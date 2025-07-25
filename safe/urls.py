from django.http import HttpResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.contrib import admin

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
    path('welcome/', lambda request: HttpResponse("Добро пожаловать в API клиники Safe!")),
    path('admin/', admin.site.urls),

    # API приложения
    path('api/', include('main.urls')),
    path('api/services/', include('services.urls')),
    path('api/list_doctor/', include('listdoctors.urls')),
    path('api/list_patients/', include('listpatients.urls')),
    path('api/branches/', include('branch.urls')),

    # JWT
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
