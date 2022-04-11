from rest_framework import permissions

from .models import UserRole


class IsModeratorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.moderator)


class IsAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.admin
                     or request.user.is_superuser))


class IsSuperuserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.superuser
                and request.user.is_superuser))
