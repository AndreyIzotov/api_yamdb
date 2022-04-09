from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and ((request.user.role == 'admin')
                     or request.user.is_superuser))


class MainPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(request.user.is_staff or request.user.role == 'admin')
