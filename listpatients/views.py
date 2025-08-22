from rest_framework import viewsets

from .models import Patient
from .permissions import IsAdminOrDoctor
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAdminOrDoctor]