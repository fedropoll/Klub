from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from main.views import (
    RegisterAPIView,
    ClientRegisterAPIView,
    VerifyEmailAPIView
)

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="Документация API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Сотрудники
    path('register/', RegisterAPIView.as_view(), name='register'),

    # Клиенты
    path('register/client/', ClientRegisterAPIView.as_view(), name='register-client'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
