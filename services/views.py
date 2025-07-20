from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .models import Service
from .serializers import ServiceSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Управление услугами",
        operation_description="Позволяет создавать, редактировать, просматривать и удалять медицинские услуги."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
