from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AdminTokenView, DirectorTokenView, DoctorTokenView, ClientTokenView

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

    path('api/token/admin/', AdminTokenView.as_view(), name='admin_token'),
    path('api/token/director/', DirectorTokenView.as_view(), name='token_director'),
    path('api/token/doctor/', DoctorTokenView.as_view(), name='token_doctor'),
    path('api/token/client/', ClientTokenView.as_view(), name='token_client'),

    path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),
]
