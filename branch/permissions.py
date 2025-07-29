from rest_framework.permissions import BasePermission, SAFE_METHODS
from main.permissions import IsAdminOrDirector


class ReadOnlyOrAdminOrDirector(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated

        return IsAdminOrDirector().has_permission(request, view)