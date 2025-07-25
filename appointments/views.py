# appointments/views.py

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Appointment, TIME_SLOTS
from .serializers import AppointmentSerializer

import calendar
from datetime import datetime


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        doctor = request.data.get('doctor')
        date = request.data.get('date')
        time_slot = request.data.get('time_slot')

        if Appointment.objects.filter(doctor=doctor, date=date, time_slot=time_slot).exists():
            raise ValidationError("Это время уже занято. Пожалуйста, выберите другое.")

        return super().create(request, *args, **kwargs)


class AvailableTimeSlotsView(APIView):
    def get(self, request):
        doctor_id = request.GET.get('doctor')
        date = request.GET.get('date')

        if not doctor_id or not date:
            return Response({"error": "Не хватает параметров: doctor и date"}, status=400)

        taken_slots = Appointment.objects.filter(
            doctor_id=doctor_id,
            date=date
        ).values_list('time_slot', flat=True)

        available_slots = [slot for slot, _ in TIME_SLOTS if slot not in taken_slots]

        return Response({"available_slots": available_slots})


class CalendarUIPickerView(APIView):
    def get(self, request):
        today = datetime.today()
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))
        selected = request.GET.get('selected')

        MONTH_NAMES_RU = [
            "Янв", "Фев", "Мар", "Апр", "Май", "Июн",
            "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"
        ]
        WEEKDAYS_RU = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]

        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(year, month)
        month_grid = [
            [f"{year}-{month:02d}-{day:02d}" if day != 0 else "" for day in week]
            for week in month_days
        ]

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