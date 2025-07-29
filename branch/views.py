# branch/views.py

from rest_framework import viewsets
from .models import Branch
from .serializers import BranchSerializer
from .permissions import ReadOnlyOrAdminOrDirector # Using our custom permission

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [ReadOnlyOrAdminOrDirector] # Reading for all, writing for admin/director