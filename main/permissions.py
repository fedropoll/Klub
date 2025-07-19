# main/permissions.py
from rest_framework import permissions

class IsAdminOrDirector(permissions.BasePermission):
    """
    Custom permission to only allow users with 'admin' or 'director' role to access.
    """
    def has_permission(self, request, view):
        # Проверяем, аутентифицирован ли пользователь
        if not request.user.is_authenticated:
            return False

        # Проверяем, имеет ли пользователь профиль и соответствующую роль
        if hasattr(request.user, 'userprofile'):
            return request.user.userprofile.role in ['admin', 'director']
        return False

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow users with 'admin' role to access.
    """
    def has_permission(self, request, view):
        # Проверяем, аутентифицирован ли пользователь
        if not request.user.is_authenticated:
            return False

        # Проверяем, имеет ли пользователь профиль и роль 'admin'
        if hasattr(request.user, 'userprofile'):
            return request.user.userprofile.role == 'admin'
        return False