from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import BranchViewSet

router = DefaultRouter()
router.register(r'branches', BranchViewSet, basename='branch')

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # если нужен токен, иначе можно убрать
]

urlpatterns += router.urls
