from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    UserRegisterView,
    VerifyEmailView,
    ResendVerificationCodeView,
    CurrentUserView,
    AppointmentListView,
    AppointmentDetailView,
    PaymentListView,
    PaymentDetailView,
    AppointmentCreateView,
)

urlpatterns = [
    path('auth/register/', UserRegisterView.as_view(), name='register'),
    path('auth/verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('auth/resend-code/', ResendVerificationCodeView.as_view(), name='resend_code'),
    path('profile/me/', CurrentUserView.as_view(), name='current_user_profile'),

    path('appointments/', AppointmentListView.as_view(), name='appointment_list'),
    path('appointments/create/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment_detail'),

    path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),
]