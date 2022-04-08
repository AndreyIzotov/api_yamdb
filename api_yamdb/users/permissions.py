from rest_framework import permissions


class IsModeratorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == 'moderator'))


class IsAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and ((request.user.role == 'admin')
                     or request.user.is_superuser))


class IsSuperuserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return ((request.user.is_authenticated
                and (request.user.role == 'superuser'))
                and request.user.is_superuser)
