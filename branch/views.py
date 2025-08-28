# branch/views.py

from rest_framework import viewsets
from .models import Branch
from .permissions import IsAdminOrDoctor
from .serializers import BranchSerializer

class BranchViewSet(viewsets.ModelViewSet):

    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAdminOrDoctor]