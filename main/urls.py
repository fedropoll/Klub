# /home/asylbek/Desktop/klub/safe/main/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterAPIView,
    ClientRegisterAPIView,
    VerifyEmailAPIView,
    ResendVerifyCodeAPIView,
    BranchViewSet,
)

router = DefaultRouter()
router.register(r'branches', BranchViewSet, basename='branch')

urlpatterns = [
    path('register/staff/', RegisterAPIView.as_view(), name='register-staff'),
    path('register/client/', ClientRegisterAPIView.as_view(), name='register-client'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('resend-code/', ResendVerifyCodeAPIView.as_view(), name='resend-code'),

    path('', include(router.urls)),
]