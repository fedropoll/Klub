from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from main.permissions import IsAdminOrDirector
from .models import Branch, Service
from .serializers import BranchSerializer, ServiceSerializer

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsAdminOrDirector],[AllowAny]

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrDirector],[AllowAny]