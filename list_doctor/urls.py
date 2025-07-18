# list_doctor/urls.py
from django.urls import path
from .views import (
    BranchListCreateAPIView,
    BranchRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('branches/', BranchListCreateAPIView.as_view(), name='branch-list-create'),
    path('branches/<int:pk>/', BranchRetrieveUpdateDestroyAPIView.as_view(), name='branch-detail'),
]