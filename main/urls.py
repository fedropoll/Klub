from django.urls import path
from .views import (
    ClientRegisterAPIView, VerifyEmailAPIView,
    ResendVerifyCodeAPIView, StaffRegisterAPIView
)

urlpatterns = [
    path('register/client/', ClientRegisterAPIView.as_view(), name='register_client'),
    path('register/staff/', StaffRegisterAPIView.as_view(), name='register_staff'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify_email'),
    path('resend-verify-code/', ResendVerifyCodeAPIView.as_view(), name='resend_verify_code'),
]
