from rest_framework.permissions import BasePermission

class IsAdminDoctorOrDirector(BasePermission):
    """
    Разрешает доступ только аутентифицированным пользователям с ролями:
    'admin', 'doctor' или 'director'.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        role = getattr(request.user.userprofile, 'role', None)
        return role in ['admin', 'doctor', 'director']
