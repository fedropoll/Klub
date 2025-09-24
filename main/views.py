from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from drf_yasg.utils import swagger_auto_schema

from listdoctors.models import Doctor
from listdoctors.serializers import DoctorSerializer
from .serializers import (
    UserRegistrationSerializer,
    CurrentUserSerializer,
    AppointmentSerializer,
    AppointmentCreateSerializer,
    PaymentSerializer,
    ResendCodeSerializer,
    VerifyEmailSerializer,
    AdminTokenObtainPairSerializer,
    DirectorTokenObtainPairSerializer,
    DoctorTokenObtainPairSerializer,
    ClientTokenObtainPairSerializer, UserProfileSerializer, ClientProfileSerializer,
)
from .models import CustomUser, ClientProfile, EmailVerificationCode, Appointment, Payment
from django.conf import settings
from django.core.mail import send_mail
import random
from django.utils import timezone
from rest_framework_simplejwt.views import TokenObtainPairView

# ------------------- Регистрация -------------------
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

        try:
            send_mail(
                subject='Код подтверждения для вашего аккаунта',
                message=f'Ваш код подтверждения: {code}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,  # можешь поставить True, если хочешь, чтобы оно просто молчало
            )
        except Exception as e:
            # Логируем ошибку и выводим код в консоль
            print(f"[DEBUG] Ошибка при отправке email: {e}")
            print(f"[DEBUG] Код подтверждения для {user.email}: {code}")



# ------------------- Email verification -------------------
class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser]

    @swagger_auto_schema(request_body=VerifyEmailSerializer)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

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
            return Response({'detail': 'Неверный код подтверждения или пользователь.'}, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationCodeView(generics.GenericAPIView):
    serializer_class = ResendCodeSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser]

    @swagger_auto_schema(request_body=ResendCodeSerializer)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = CustomUser.objects.get(email=email)
            UserRegisterView()._send_verification_email(user)
            return Response({'detail': 'Новый код подтверждения отправлен на ваш email.'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)

from rest_framework_simplejwt.views import TokenObtainPairView

class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer

class DirectorTokenObtainPairView(TokenObtainPairView):
    serializer_class = DirectorTokenObtainPairSerializer

class DoctorTokenObtainPairView(TokenObtainPairView):
    serializer_class = DoctorTokenObtainPairSerializer

class ClientTokenObtainPairView(TokenObtainPairView):
    serializer_class = ClientTokenObtainPairSerializer


# class AdminTokenObtainPairView(TokenObtainPairView):
#     serializer_class = AdminTokenObtainPairSerializer
#
# # === DIRECTOR ===
# class DirectorTokenView(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         password = request.data.get('password')
#
#         try:
#             user = CustomUser.objects.get(email=email)
#         except CustomUser.DoesNotExist:
#             return Response({"detail": "Директор с таким email не найден"}, status=status.HTTP_404_NOT_FOUND)
#
#         if not user.check_password(password):
#             return Response({"detail": "Неверный пароль"}, status=status.HTTP_400_BAD_REQUEST)
#
#         if user.user_profile.role != "director":
#             return Response({"detail": "Этот токен доступен только для директоров"}, status=status.HTTP_403_FORBIDDEN)
#
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             "refresh": str(refresh),
#             "access": str(refresh.access_token),
#             "role": user.user_profile.role
#         }, status=status.HTTP_200_OK)
#
#
# class DoctorTokenView(TokenObtainPairView):
#     serializer_class = DoctorTokenSerializer
#
#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         password = request.data.get('password')
#
#         try:
#             user = CustomUser.objects.get(email=email)
#         except CustomUser.DoesNotExist:
#             return Response({"detail": "Доктор с таким email не найден"}, status=status.HTTP_404_NOT_FOUND)
#
#         if not user.check_password(password):
#             return Response({"detail": "Неверный пароль"}, status=status.HTTP_400_BAD_REQUEST)
#
#         if user.user_profile.role != "doctor":
#             return Response({"detail": "Этот токен доступен только для докторов"}, status=status.HTTP_403_FORBIDDEN)
#
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             "refresh": str(refresh),
#             "access": str(refresh.access_token),
#             "role": user.user_profile.role
#         }, status=status.HTTP_200_OK)
#
#
# # === CLIENT ===
# class ClientTokenView(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         password = request.data.get('password')
#
#         try:
#             user = CustomUser.objects.get(email=email)
#         except CustomUser.DoesNotExist:
#             return Response({"detail": "Клиент с таким email не найден"}, status=status.HTTP_404_NOT_FOUND)
#
#         if not user.check_password(password):
#             return Response({"detail": "Неверный пароль"}, status=status.HTTP_400_BAD_REQUEST)
#
#         if user.user_profile.role != "client":
#             return Response({"detail": "Этот токен доступен только для клиентов"}, status=status.HTTP_403_FORBIDDEN)
#
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             "refresh": str(refresh),
#             "access": str(refresh.access_token),
#             "role": user.user_profile.role
#         }, status=status.HTTP_200_OK)

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
