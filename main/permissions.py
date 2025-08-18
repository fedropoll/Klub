from rest_framework import permissions

from rest_framework import permissions

class IsAdminOrDirector(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'user_profile') and request.user.user_profile.role in ['admin','director']



class IsStaffOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if hasattr(user, 'user_profile'):
            return user.user_profile.role != 'patient'
        return False


class IsOwnerOrAdminOrDirector(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        if hasattr(obj, 'user') and obj.user == request.user:
            return True

        return IsAdminOrDirector().has_permission(request, view)

class IsInRole(permissions.BasePermission):
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return hasattr(user, 'user_profile') and user.user_profile.role in self.allowed_roles
