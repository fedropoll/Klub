from rest_framework import generics, permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    MyTokenObtainPairSerializer,
    DirectorTokenSerializer, DoctorTokenSerializer,
    ClientTokenSerializer,
    UserRegistrationSerializer,
    UserProfileSerializer,
    ClientProfileSerializer,
    CurrentUserSerializer,
    AppointmentSerializer,
    PaymentSerializer,
    AppointmentCreateSerializer,
    ResendCodeSerializer,
    VerifyEmailSerializer, AdminTokenObtainPairSerializer,
)
from .models import CustomUser, ClientProfile, EmailVerificationCode, Appointment, Payment
from listdoctors.models import Doctor
from listdoctors.serializers import DoctorSerializer
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
        code = str(random.randint(100000, 999999))
        EmailVerificationCode.objects.update_or_create(
            user=user,
            defaults={'code': code, 'is_used': False, 'created_at': timezone.now()}
        )
        subject = 'Код подтверждения для вашего аккаунта'
        message = f'Ваш код подтверждения: {code}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, email_from, recipient_list)


@swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'code'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL,
                                    description='Email пользователя'),
            'code': openapi.Schema(type=openapi.TYPE_STRING, description='Код подтверждения из письма', min_length=6,
                                   max_length=6),
        }
    ),
    responses={
        200: openapi.Response(description='Email успешно подтвержден!'),
        400: openapi.Response(description='Неверный код или истек срок действия'),
        404: openapi.Response(description='Пользователь не найден')
    }
)
class VerifyEmailView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = VerifyEmailSerializer
    parser_classes = [JSONParser]

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


# --- TOKEN VIEWS WITH EXISTENCE CHECK ---

# class AdminTokenView(TokenObtainPairView):
#     serializer_class = AdminTokenSerializer
#
#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user = CustomUser.objects.filter(email=email).first()
#         if not user:
#             user = CustomUser.objects.create_superuser(email=email, password=password)
#         refresh = RefreshToken.for_user(user)
#         return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)


class DirectorTokenView(TokenObtainPairView):
    serializer_class = DirectorTokenSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            user = CustomUser.objects.create_user(email=email, password=password)
            # добавь роль director
            user.user_profile.role = 'director'
            user.user_profile.save()
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)



class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer

class DoctorTokenView(TokenObtainPairView):
    serializer_class = DoctorTokenSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            user = CustomUser.objects.create_user(email=email, password=password)
            user.user_profile.role = 'doctor'
            user.user_profile.save()
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)


class ClientTokenView(TokenObtainPairView):
    serializer_class = ClientTokenSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            user = CustomUser.objects.create_user(email=email, password=password)
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)


# --- CURRENT USER ---

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

        doctor_profile_data = request.data.get('doctor_profile')
        if doctor_profile_data and user.user_profile.role in ['doctor', 'director']:
            doctor_profile, created = Doctor.objects.get_or_create(user_profile=user.user_profile)
            doctor_serializer = DoctorSerializer(doctor_profile, data=doctor_profile_data, partial=partial)
            doctor_serializer.is_valid(raise_exception=True)
            doctor_serializer.save()

        return Response(self.get_serializer(user).data)


# --- APPOINTMENTS ---

class AppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'client_profile'):
            return Appointment.objects.filter(client=self.request.user.client_profile).order_by('-start_time')
        return Appointment.objects.none()


class AppointmentDetailView(generics.RetrieveAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Appointment.objects.all()

    def get_queryset(self):
        if hasattr(self.request.user, 'client_profile'):
            return Appointment.objects.filter(client=self.request.user.client_profile)
        return Appointment.objects.none()


class AppointmentCreateView(generics.CreateAPIView):
    serializer_class = AppointmentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


# --- PAYMENTS ---

class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'client_profile'):
            return Payment.objects.filter(client=self.request.user.client_profile).order_by('-payment_date')
        return Payment.objects.none()


class PaymentDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Payment.objects.all()

    def get_queryset(self):
        if hasattr(self.request.user, 'client_profile'):
            return Payment.objects.filter(client=self.request.user.client_profile)
        return Payment.objects.none()
