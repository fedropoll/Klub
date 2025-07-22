from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from datetime import date
from .models import Doctor
from .serializers import DoctorSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    parser_classes = [MultiPartParser, FormParser]

    @action(detail=False, methods=['get'], url_path='search')
    def search_doctors(self, request):
        queryset = self.queryset

        # Роль (тег)
        tags = request.query_params.get('tags')
        if tags:
            queryset = queryset.filter(tags=tags)

        # Пол
        gender = request.query_params.get('gender')
        if gender:
            queryset = queryset.filter(gender=gender)

        # Возрастной диапазон
        age_range = request.query_params.get('age_range')
        if age_range:
            try:
                min_age, max_age = map(int, age_range.split('-'))
                today = date.today()
                max_birthdate = date(today.year - min_age, today.month, today.day)
                min_birthdate = date(today.year - max_age - 1, today.month, today.day)
                queryset = queryset.filter(birth_date__range=(min_birthdate, max_birthdate))
            except:
                pass  # просто игнорим, если криво введено

        serializer = DoctorSerializer(queryset, many=True)
        return Response(serializer.data)
