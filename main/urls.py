from django.urls import path
from .views import UserRegisterView, VerifyEmailView, ResendVerificationCodeView, CurrentUserView

urlpatterns = [
    path('api/auth/register/', UserRegisterView.as_view(), name='register'),  # <--- Обрати внимание на запятую
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('resend-code/', ResendVerificationCodeView.as_view(), name='resend_code'),
    path('me/', CurrentUserView.as_view(), name='current_user_profile'),
]
