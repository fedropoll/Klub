# listpatients/views.py

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Patient
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [AllowAny]