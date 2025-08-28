from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from main.views import DoctorTokenView, ClientTokenView, DirectorTokenView

# Настройка Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API Клиники Safe v1",
        default_version='v1',
        description="Документация по API.",
        contact=openapi.Contact(email="contact@safe.com"),
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),


    # Основные приложения
    path('services/', include('services.urls')),
    path('list_doctor/', include('listdoctors.urls')),
    path('list_patients/', include('listpatients.urls')),
    path('branches/', include('branch.urls')),
    path('appointments/', include('appointments.urls')),
    path('analytics/', include('data_analytics.urls')),
    path('', include('main.urls')),

    # Swagger и Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Для статических и медиа файлов (только в DEBUG)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
