import django_filters
from .models import Appointment

class AppointmentFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Appointment
        fields = ['date', 'doctor', 'patient']