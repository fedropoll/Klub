from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Sum, Count
from django.db.models.functions import ExtractWeekDay
from django.utils import timezone
from datetime import timedelta

from main.models import Payment, Appointment, ClientProfile # Импортируем модели из main
from .serializers import AnalyticsDashboardSerializer



class AnalyticsDashboardView(APIView):
    permission_classes = [permissions.IsAdminUser] # Только для администраторов или директоров

    def get(self, request):
        end_date = timezone.now()
        start_date_current_period = end_date - timedelta(days=7) # Последние 7 дней
        start_date_previous_period = start_date_current_period - timedelta(days=7) # Предыдущие 7 дней

        # Общая прибыль
        total_profit_current = Payment.objects.filter(
            payment_date__range=(start_date_current_period, end_date),
            status='paid'
        ).aggregate(total=Sum('amount'))['total'] or 0

        total_profit_previous = Payment.objects.filter(
            payment_date__range=(start_date_previous_period, start_date_current_period),
            status='paid'
        ).aggregate(total=Sum('amount'))['total'] or 0

        profit_change_percentage = 0
        if total_profit_previous > 0:
            profit_change_percentage = ((total_profit_current - total_profit_previous) / total_profit_previous) * 100

        # Всего клиентов
        total_clients_current = ClientProfile.objects.filter(
            user_date_joined_range=(start_date_current_period, end_date)
        ).count()

        total_clients_previous = ClientProfile.objects.filter(
            user_date_joined_range=(start_date_previous_period, start_date_current_period)
        ).count()

        clients_change_percentage = 0
        if total_clients_previous > 0:
            clients_change_percentage = ((total_clients_current - total_clients_previous) / total_clients_previous) * 100

        # Посещения по дням
        visits_by_day_data = Appointment.objects.filter(
            start_time__range=(start_date_current_period, end_date)
        ).annotate(
            day=ExtractWeekDay('start_time')
        ).values('day').annotate(count=Count('id')).order_by('day')

        visits_labels = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
        visits_data = [0] * 7
        for item in visits_by_day_data:
            # ExtractWeekDay возвращает 1 для воскресенья, 2 для понедельника... 7 для субботы
            # Преобразуем в 0 для ПН, 1 для ВТ ... 6 для ВС
            day_index = (item['day'] - 2) % 7
            visits_data[day_index] = item['count']

        # Прибыль по дням
        profit_by_day_data = Payment.objects.filter(
            payment_date__range=(start_date_current_period, end_date),
            status='paid'
        ).annotate(
            day=ExtractWeekDay('payment_date')
        ).values('day').annotate(total_amount=Sum('amount')).order_by('day')

        profit_labels = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
        profit_data = [0.0] * 7
        for item in profit_by_day_data:
            day_index = (item['day'] - 2) % 7
            profit_data[day_index] = float(item['total_amount'])

        response_data = {
            "total_profit": {
                "value": total_profit_current,
                "change_percentage": round(profit_change_percentage, 2),
                "description": "Общая прибыль"
            },
            "total_clients": {
                "value": total_clients_current,
                "change_percentage": round(clients_change_percentage, 2),
                "description": "Всего клиентов"
            },
            "visits_by_day": {
                "labels": visits_labels,
                "data": visits_data
            },
            "profit_by_day": {
                "labels": profit_labels,
                "data": profit_data
            }
        }
        serializer = AnalyticsDashboardSerializer(response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

