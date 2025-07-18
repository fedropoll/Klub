# list_doctor/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .models import Branch # Импортируем Branch из этого же приложения
from .serializers import BranchSerializer # Импортируем BranchSerializer из этого же приложения

class BranchListCreateAPIView(generics.ListCreateAPIView):
    """
    API для получения списка филиалов и создания нового филиала.
    Требуется аутентификация (JWT токен).
    """
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated] # Защищаем API, требуется аутентификация

    @swagger_auto_schema(
        operation_summary="Получить список филиалов или создать новый (list_doctor)",
        responses={200: BranchSerializer(many=True), 201: BranchSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать новый филиал (list_doctor)",
        request_body=BranchSerializer,
        responses={201: BranchSerializer()}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BranchRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API для получения, обновления или удаления конкретного филиала.
    Требуется аутентификация (JWT токен).
    """
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated] # Защищаем API
    lookup_field = 'pk' # Используем primary key для поиска филиала

    @swagger_auto_schema(
        operation_summary="Получить информацию о филиале по ID (list_doctor)",
        responses={200: BranchSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить информацию о филиале по ID (list_doctor)",
        request_body=BranchSerializer,
        responses={200: BranchSerializer()}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частично обновить информацию о филиале по ID (list_doctor)",
        request_body=BranchSerializer,
        responses={200: BranchSerializer()}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить филиал по ID (list_doctor)",
        responses={204: "No Content"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)