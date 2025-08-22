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
