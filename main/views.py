from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import CustomUser, UserProfile, ClientProfile, EmailVerificationCode
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    ClientProfileSerializer,
    CurrentUserSerializer,
    AppointmentSerializer,
    PaymentSerializer,
    AppointmentCreateSerializer,
    ResendCodeSerializer,
    VerifyEmailSerializer,
    ChangePasswordSerializer,
    UserListSerializer,
    SendCodeByPhoneSerializer,
    SendSMSMessageSerializer  # Импортируем новый сериализатор
)
from .utils import send_whatsapp_message, send_telegram_message, send_sms_message  # Импортируем новую функцию
from django.conf import settings
from django.core.mail import send_mail
import random
from django.utils import timezone
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)


class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        self._send_verification_email(user)
        return user

    def _send_verification_email(self, user):
        code = str(random.randint(1000, 9999))
        EmailVerificationCode.objects.update_or_create(
            user=user,
            defaults={'code': code, 'is_used': False, 'created_at': timezone.now()}
        )
        subject = 'Код подтверждения для вашего аккаунта'
        message = f'Ваш код подтверждения: {code}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        try:
            send_mail(subject, message, email_from, recipient_list)
            logger.info(f"Email verification code sent to {user.email}")
        except Exception as e:
            logger.error(f"Failed to send email verification code to {user.email}: {e}")


@swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'code'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL,
                                    description='Email пользователя'),
            'code': openapi.Schema(type=openapi.TYPE_STRING, description='Код подтверждения из письма', min_length=4,
                                   max_length=4),
        }
    ),
    responses={
        200: openapi.Response(description='Email успешно подтвержден!'),
        400: openapi.Response(description='Неверный код или истек срок действия'),
        404: openapi.Response(description='Пользователь не найден')
    }
)
class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = VerifyEmailSerializer
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
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


@swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL,
                                    description='Email пользователя'),
        }
    ),
    responses={
        200: openapi.Response(description='Новый код подтверждения отправлен на ваш email!'),
        404: openapi.Response(description='Пользователь не найден')
    }
)
class ResendVerificationCodeView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResendCodeSerializer
    queryset = CustomUser.objects.none()
    parser_classes = [JSONParser]

    def create(self, request, *args, **kwargs):
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

        user_profile_data = request.data.get('user_profile')
        if user_profile_data:
            user_profile_serializer = UserProfileSerializer(user.user_profile, data=user_profile_data, partial=partial)
            user_profile_serializer.is_valid(raise_exception=True)
            user_profile_serializer.save()

        client_profile_data = request.data.get('client_profile')
        if client_profile_data:
            client_profile, created = ClientProfile.objects.get_or_create(user=user)
            client_profile_serializer = ClientProfileSerializer(client_profile, data=client_profile_data,
                                                                partial=partial)
            client_profile_serializer.is_valid(raise_exception=True)
            client_profile_serializer.save()

        return Response(self.get_serializer(user).data)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Неверный пароль."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            return Response({"detail": "Пароль успешно изменен."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all().select_related('user_profile', 'client_profile')
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAdminUser]


@swagger_auto_schema(
    request_body=SendCodeByPhoneSerializer,
    responses={
        200: openapi.Response(description='Код подтверждения отправлен на указанный номер.'),
        400: openapi.Response(description='Неверные данные запроса или ошибка отправки.'),
        404: openapi.Response(description='Пользователь или код подтверждения не найден.')
    }
)
class SendCodeByPhoneView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SendCodeByPhoneSerializer
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number')
        method = serializer.validated_data.get('method')

        try:
            user = CustomUser.objects.get(email=email)
            verification_code_obj = EmailVerificationCode.objects.filter(
                user=user, is_used=False, created_at__gt=timezone.now() - timedelta(minutes=10)
            ).order_by('-created_at').first()

            if not verification_code_obj:
                code = str(random.randint(1000, 9999))
                verification_code_obj = EmailVerificationCode.objects.create(
                    user=user, code=code, created_at=timezone.now(), is_used=False
                )
                logger.info(f"New verification code generated for {user.email}: {code}")
            else:
                code = verification_code_obj.code
                logger.info(f"Reusing existing verification code for {user.email}: {code}")

            message_text = f"Ваш код подтверждения для Safe Clinic: {code}"
            success = False
            error_message = ""

            if method == 'whatsapp':
                if not phone_number.startswith('whatsapp:'):
                    phone_number = f"whatsapp:{phone_number}"
                success, error_message = send_whatsapp_message(to_phone_number=phone_number, message=message_text)
            elif method == 'telegram':
                success, error_message = send_telegram_message(chat_id=phone_number, message=message_text)

            if success:
                return Response({'detail': f'Код подтверждения отправлен на {phone_number} через {method}.'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'detail': f'Не удалось отправить код подтверждения: {error_message}'},
                                status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error in SendCodeByPhoneView: {e}")
            return Response({'detail': 'Произошла внутренняя ошибка сервера.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    request_body=SendSMSMessageSerializer,
    responses={
        200: openapi.Response(description='Сообщение SMS успешно отправлено.'),
        400: openapi.Response(description='Неверные данные запроса или ошибка отправки.'),
    }
)
class SendSMSMessageView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SendSMSMessageSerializer
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.get('phone_number')
        message = serializer.validated_data.get('message')

        success, error_message = send_sms_message(to_phone_number=phone_number, message=message)

        if success:
            return Response({'detail': 'Сообщение SMS успешно отправлено.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': f'Не удалось отправить SMS: {error_message}'},
                            status=status.HTTP_400_BAD_REQUEST)
