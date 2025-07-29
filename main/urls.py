from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegisterView,
    VerifyEmailView,
    ResendVerificationCodeView,
    CurrentUserView,
    # ChangePasswordView
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('resend-code/', ResendVerificationCodeView.as_view(), name='resend_code'),
    path('me/', CurrentUserView.as_view(), name='current_user_profile'),
    # path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]
