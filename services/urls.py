from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, CategoryViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = router.urls