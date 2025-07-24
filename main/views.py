from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import (
    ClientRegisterSerializer,
    VerifyEmailSerializer,
    ResendVerifyCodeSerializer,
    StaffRegisterSerializer
)

class ClientRegisterAPIView(generics.CreateAPIView):
    serializer_class = ClientRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Регистрация прошла успешно. Проверьте почту."}, status=status.HTTP_201_CREATED)

class VerifyEmailAPIView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Email успешно подтвержден"}, status=status.HTTP_201_CREATED)

class ResendVerifyCodeAPIView(generics.GenericAPIView):
    serializer_class = ResendVerifyCodeSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Новый код подтверждения отправлен"}, status=status.HTTP_201_CREATED)

class StaffRegisterAPIView(generics.CreateAPIView):
    serializer_class = StaffRegisterSerializer
    permission_classes = [AllowAny]
