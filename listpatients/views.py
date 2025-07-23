from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Patient, Appointment
from .serializers import PatientSerializer, AppointmentSerializer
# views.py
import calendar
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response

class CalendarUIPickerView(APIView):
    def get(self, request):
        today = datetime.today()
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))
        selected = request.GET.get('selected')  # формат: '2024-01-18'

        # Название месяца
        MONTH_NAMES_RU = [
            "Янв", "Фев", "Мар", "Апр", "Май", "Июн",
            "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"
        ]

        # Дни недели
        WEEKDAYS_RU = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]

        # Получаем календарную сетку
        cal = calendar.Calendar(firstweekday=0)  # ПН = 0
        month_days = cal.monthdayscalendar(year, month)
        month_grid = []
        for week in month_days:
            formatted_week = [
                f"{year}-{month:02d}-{day:02d}" if day != 0 else ""
                for day in week
            ]
            month_grid.append(formatted_week)

        response = {
            "year": year,
            "month": month,
            "month_name": MONTH_NAMES_RU[month - 1],
            "weekdays": WEEKDAYS_RU,
            "weeks": month_grid,
            "today": today.strftime("%Y-%m-%d"),
            "selected": selected or ""
        }

        return Response(response)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes =[AllowAny]


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes =[AllowAny]
