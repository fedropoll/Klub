from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from main.permissions import IsAdminOrDirector
from .models import Service
from .serializers import ServiceSerializer
from django_filters.rest_framework import DjangoFilterBackend
import logging

logger = logging.getLogger(__name__)

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterer_fields = ['is_active', 'branch']

    @swagger_auto_schema(operation_summary="Список услуг", operation_description="Возвращает список всех медицинских услуг.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Создание услуги", operation_description="Создает новую медицинскую услугу.")
    def create(self, request, *args, **kwargs):
        logger.info(f"Received data (create): {request.data}")
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Обновление услуги", operation_description="Обновляет существующую медицинскую услугу.")
    def update(self, request, *args, **kwargs):
        logger.info(f"Received data (update): {request.data}")
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Удаление услуги", operation_description="Удаляет медицинскую услугу.")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
