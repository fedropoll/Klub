from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    RegisterSerializer,
    ClientRegisterSerializer,
    VerifyEmailSerializer
)
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import User
from .models import ClientProfile

# 👉 Сотрудники
class RegisterAPIView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Сотрудник зарегистрирован'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 👉 Клиенты
class ClientRegisterAPIView(APIView):
    @swagger_auto_schema(request_body=ClientRegisterSerializer)
    def post(self, request):
        serializer = ClientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Код отправлен на почту'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailAPIView(APIView):
    @swagger_auto_schema(request_body=VerifyEmailSerializer)
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']

            try:
                user = User.objects.get(email=email)
                profile = user.clientprofile

                if profile.confirmation_code == code:
                    user.is_active = True
                    user.save()
                    profile.is_email_verified = True
                    profile.save()
                    return Response({'message': 'Email подтвержден'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Неверный код'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
