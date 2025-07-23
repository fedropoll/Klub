from django.contrib import admin
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

from main.admin import my_admin_site
from main.views import (
    RegisterAPIView,
    ClientRegisterAPIView,
    VerifyEmailAPIView,
    ResendVerifyCodeAPIView,
)


schema_view = get_schema_view(
    openapi.Info(
        title="API Клиники Safe v1",
        default_version='v1',
        description="Документация по API.",
        terms_of_service="http://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@safeClinic.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', my_admin_site.urls),

    # Регистрация и подтверждение email
    path('api/register/', RegisterAPIView.as_view(), name='register-staff'),
    path('api/register/client/', ClientRegisterAPIView.as_view(), name='register-client'),
    path('api/verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('api/resend-verify-code/', ResendVerifyCodeAPIView.as_view(), name='resend-verify-code'),

    # JWT токены
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # API приложений
    path('api/list_doctor/', include('listdoctors.urls')),
    path('api/list_patients/', include('listpatients.urls')),
    path('api/services/', include('services.urls')),
    path('api/', include('main.urls')),

    # Swagger и Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
