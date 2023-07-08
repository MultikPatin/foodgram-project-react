from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class OwnerOrAdmins(permissions.BasePermission):
    """Разрешение на уровне админ или создатель"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (obj == request.user
                or request.user.is_admin or request.user.is_superuser)


class IsAdminOrReadOnly(BasePermission):
    """Разрешение на уровне админ."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class AuthorOrReadOnly(BasePermission):
    """Разрешение на уровне создатель"""
    
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
        )
