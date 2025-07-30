from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema

from .models import CustomUser, UserProfile, ClientProfile, EmailVerificationCode
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    ClientProfileSerializer,
    CurrentUserSerializer,
    ChangePasswordSerializer,
    ResendCodeSerializer,
    VerifyEmailSerializer
)
from django.conf import settings
from django.core.mail import send_mail
import random
from django.utils import timezone


class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self._send_verification_email(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _send_verification_email(self, user):
        """Отправляет email с кодом подтверждения."""
        code = str(random.randint(1000, 9999))
        EmailVerificationCode.objects.update_or_create(
            user=user,
            defaults={'code': code, 'is_used': False, 'created_at': timezone.now()}
        )
        subject = 'Код подтверждения для вашего аккаунта'
        message = f'Ваш код подтверждения: {code}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])


class VerifyEmailView(GenericAPIView):
    """Подтверждение email по коду"""
    permission_classes = [permissions.AllowAny]
    serializer_class = VerifyEmailSerializer
    parser_classes = [JSONParser]

    @swagger_auto_schema(request_body=VerifyEmailSerializer)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        code = serializer.validated_data.get('code')

        try:
            user = CustomUser.objects.get(email=email)
            verification_code_obj = EmailVerificationCode.objects.get(user=user, code=code)

            if verification_code_obj.is_expired():
                return Response({'detail': 'Код подтверждения истек.'}, status=status.HTTP_400_BAD_REQUEST)
            if verification_code_obj.is_used:
                return Response({'detail': 'Код подтверждения уже использован.'}, status=status.HTTP_400_BAD_REQUEST)

            # Подтверждаем email
            client_profile = user.client_profile
            client_profile.is_email_verified = True
            client_profile.save()

            verification_code_obj.is_used = True
            verification_code_obj.save()

            return Response({'detail': 'Email успешно подтвержден!'}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)
        except EmailVerificationCode.DoesNotExist:
            return Response({'detail': 'Неверный код подтверждения или пользователь.'},
                            status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationCodeView(GenericAPIView):
    """Отправка нового кода подтверждения"""
    permission_classes = [permissions.AllowAny]
    serializer_class = ResendCodeSerializer
    parser_classes = [JSONParser]

    @swagger_auto_schema(request_body=ResendCodeSerializer)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')

        try:
            user = CustomUser.objects.get(email=email)
            UserRegisterView()._send_verification_email(user)
            return Response({'detail': 'Новый код подтверждения отправлен на ваш email.'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)


class CurrentUserView(generics.RetrieveUpdateAPIView):
    serializer_class = CurrentUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        user = self.get_object()

        user_serializer = self.get_serializer(user, data=request.data, partial=partial)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        # Обновление профиля пользователя
        user_profile_data = request.data.get('user_profile')
        if user_profile_data:
            user_profile_serializer = UserProfileSerializer(user.user_profile, data=user_profile_data, partial=partial)
            user_profile_serializer.is_valid(raise_exception=True)
            user_profile_serializer.save()

        # Обновление клиентского профиля
        client_profile_data = request.data.get('client_profile')
        if client_profile_data:
            client_profile, created = ClientProfile.objects.get_or_create(user=user)
            client_profile_serializer = ClientProfileSerializer(client_profile, data=client_profile_data, partial=partial)
            client_profile_serializer.is_valid(raise_exception=True)
            client_profile_serializer.save()

        return Response(self.get_serializer(user).data)
