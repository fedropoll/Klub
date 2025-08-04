from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from datetime import date
import logging

from listdoctors.models import Doctor
from listdoctors.serializers import DoctorSerializer

logger = logging.getLogger(__name__)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], url_path='search')
    def search_doctors(self, request):
        try:
            queryset = self.queryset

            tags = request.query_params.get('tags')
            if tags:
                queryset = queryset.filter(tags=tags)

            gender = request.query_params.get('gender')
            if gender:
                queryset = queryset.filter(gender=gender)

            age_range = request.query_params.get('age_range')
            if age_range:
                try:
                    min_age, max_age = map(int, age_range.split('-'))
                    today = date.today()
                    max_birthdate = date(today.year - min_age, today.month, today.day)
                    min_birthdate = date(today.year - max_age - 1, today.month, today.day)
                    queryset = queryset.filter(birth_date__range=(min_birthdate, max_birthdate))
                except ValueError:
                    return Response({"error": "Возрастной диапазон должен быть в формате '30-40'"}, status=400)

            serializer = DoctorSerializer(queryset, many=True)
            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Ошибка при поиске врачей: {e}")
            return Response({"error": "Внутренняя ошибка сервера"}, status=500)


    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Ошибка при получении списка врачей: {e}", exc_info=True)
            return Response({"detail": "Внутренняя ошибка сервера"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)