from django.contrib import admin
from django.http.response import HttpResponseRedirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions  # важно!

schema_view = get_schema_view(
    openapi.Info(
        title="Safe Clinic API",
        default_version='v1',
        description="API для Safe Clinic",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', lambda request: HttpResponseRedirect('/swagger/')),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),


    path('services/', include('services.urls')),
    path('list_doctor/', include('listdoctors.urls')),
    path('list_patients/', include('listpatients.urls')),
    path('branches/', include('branch.urls')),
    path('appointments/', include('appointments.urls')),
    path('', include('main.urls')),

    # Swagger UI
    path('swagger/', csrf_exempt(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Для статики и медиа
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
