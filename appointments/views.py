from rest_framework import viewsets
from rest_framework.decorators import action
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Appointment # Исправленный импорт
from .serializers import AppointmentSerializer
from listdoctors.models import Doctor # Убедитесь, что Doctor импортирован, если он используется в data_analytics

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated] # Добавил IsAuthenticated как базовое разрешение

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def analytics(self, request):
        doctor_id = request.query_params.get('doctor')
        if not doctor_id:
            return Response({"error": "Не передан параметр doctor"}, status=400)

        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return Response({"error": "Доктор не найден"}, status=404)

        today = timezone.now().date()
        week_ago = today - timedelta(days=7)

        qs = Appointment.objects.filter(
            doctor=doctor,
            date__gte=week_ago,
            date__lte=today
        )

        total_appointments = qs.count()
        unique_patients = qs.values('patient').distinct().count()

        load_by_day = (
            qs.values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        days_of_week = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
        weekday_counts = {day: 0 for day in days_of_week}

        for record in load_by_day:
            d = record['date']
            if d:
                weekday_index = d.weekday()
                label = days_of_week[weekday_index]
                weekday_counts[label] = record['count']

        return Response({
            "total_appointments": total_appointments,
            "unique_patients": unique_patients,
            "load_by_weekday": weekday_counts
        })
