from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta

from .models import Service, Category
from .serializers import ServiceSerializer, CategorySerializer
from .permissions import ReadOnlyOrAdminOrDirector  # Убедитесь, что этот импорт корректен


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.select_related('category', 'branch').all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_active', 'branch', 'category']
    ordering_fields = ['price', 'name', 'created_at']
    permission_classes = [ReadOnlyOrAdminOrDirector]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def analytics(self, request):
        # Получение параметров фильтрации
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        branch_id = request.query_params.get('branch_id')
        category_id = request.query_params.get('category_id')

        qs = Service.objects.all()
        if branch_id:
            qs = qs.filter(branch_id=branch_id)
        if category_id:
            qs = qs.filter(category_id=category_id)
        total_services_count = qs.count()
        total_estimated_revenue = qs.aggregate(Sum('price'))['price__sum'] or 0
        active_services = qs.filter(is_active=True).values('id', 'name', 'price', 'category__name')

        return Response({
            "total_services_count": total_services_count,
            "total_estimated_revenue": total_estimated_revenue,
            "active_services_list": list(active_services),
            # "most_popular_services": list(popular_services)
        })


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnlyOrAdminOrDirector]
