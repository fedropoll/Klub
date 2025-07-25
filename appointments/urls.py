from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, CalendarUIPickerView

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('calendar/ui/', CalendarUIPickerView.as_view(), name='calendar-ui'),
]