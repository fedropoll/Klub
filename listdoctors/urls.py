from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'', DoctorViewSet, basename='doctor')

urlpatterns = router.urls