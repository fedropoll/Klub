from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'', AppointmentViewSet, basename='appointment')

urlpatterns = router.urls