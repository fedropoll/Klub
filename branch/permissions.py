# from rest_framework.permissions import BasePermission, SAFE_METHODS
# from main.permissions import IsAdminOrDirector
#
#
# class ReadOnlyOrAdminOrDirector(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return request.user and request.user.is_authenticated
#
#         return IsAdminOrDirector().has_permission(request, view)
from rest_framework import permissions

class IsAdminOrDoctor(permissions.BasePermission):
    """
    Разрешает доступ только пользователям с ролью 'admin' или 'doctor'.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return hasattr(user, 'user_profile') and user.user_profile.role in ['admin', 'doctor']
