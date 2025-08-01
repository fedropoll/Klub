from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserRegisterView,
    VerifyEmailView,
    ResendVerificationCodeView,
    CurrentUserView,
    UserListViewSet,
    SendCodeByPhoneView,
    SendSMSMessageView
)

router = DefaultRouter()
router.register(r'users', UserListViewSet)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('resend-code/', ResendVerificationCodeView.as_view(), name='resend_code'),
    path('me/', CurrentUserView.as_view(), name='current_user_profile'),
    path('send-code-by-phone/', SendCodeByPhoneView.as_view(), name='send_code_by_phone'),
    path('send-sms-message/', SendSMSMessageView.as_view(), name='send_sms_message'), # Новый путь
    path('', include(router.urls)),
]
