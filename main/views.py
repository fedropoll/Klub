from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser, UserProfile, ClientProfile, EmailVerificationCode
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    ClientProfileSerializer,
    CurrentUserSerializer,
    # ChangePasswordSerializer # Убрано
)
from django.conf import settings
from django.core.mail import send_mail
import random
from django.utils import timezone


class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        self._send_verification_email(user)
        return user

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


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

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


class ResendVerificationCodeView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
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


# class ChangePasswordView(generics.UpdateAPIView): # Убрано
#     serializer_class = ChangePasswordSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         return self.request.user

#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             if not self.object.check_password(serializer.data.get("old_password")):
#                 return Response({"old_password": ["Неверный пароль."]}, status=status.HTTP_400_BAD_REQUEST)

#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()

#             return Response({"detail": "Пароль успешно изменен."}, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
