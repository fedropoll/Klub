from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import User
from .models import ClientProfile

from .serializers import (
    RegisterSerializer,
    ClientRegisterSerializer,
    VerifyEmailSerializer,
    ResendVerifyCodeSerializer,
)

# 👉 Сотрудники
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_summary="Регистрация нового сотрудника",
        operation_description="Регистрирует нового пользователя с определенной ролью (например, admin, doctor, director) и немедленно активирует его аккаунт.",
        request_body=RegisterSerializer,
        responses={201: 'Сотрудник зарегистрирован. Аккаунт активен.', 400: 'Ошибка валидации'}
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Сотрудник зарегистрирован. Аккаунт активен.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 👉 Клиенты
class ClientRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_summary="Регистрация нового клиента",
        operation_description="Регистрирует нового клиента и отправляет уникальный код подтверждения на указанный email. Аккаунт клиента будет неактивным до подтверждения email. Используется для регистрации пользователей, не являющихся сотрудниками.",
        request_body=ClientRegisterSerializer,
        responses={201: 'Код подтверждения отправлен на почту. Пожалуйста, подтвердите ваш email.', 400: 'Ошибка валидации'}
    )
    def post(self, request):
        serializer = ClientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Код подтверждения отправлен на почту. Пожалуйста, подтвердите ваш email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailAPIView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_summary="Подтверждение email клиента",
        operation_description="Активирует аккаунт клиента с помощью кода подтверждения, полученного по email. Код действителен в течение 5 минут.",
        request_body=VerifyEmailSerializer,
        responses={200: 'Email успешно подтвержден. Ваш аккаунт активен.', 400: 'Неверный код или истек срок действия'}
    )
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Email успешно подтвержден. Ваш аккаунт активен.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResendVerifyCodeAPIView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_summary="Запрос нового кода подтверждения email",
        operation_description="Отправляет новый код подтверждения на email клиента, если предыдущий код истек или был утерян. Только для неподтвержденных клиентов.",
        request_body=ResendVerifyCodeSerializer,
        responses={200: 'Новый код подтверждения отправлен на вашу почту.', 400: 'Пользователь не найден или email уже подтвержден'}
    )
    def post(self, request):
        serializer = ResendVerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Новый код подтверждения отправлен на вашу почту.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Представления для филиалов остаются в list_doctor/views.py