from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Право доступа для аутентифицированного пользователя.
    Право чтения для анонима.
    Остальные права в соответствии с ролями.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        ) or (request.user.is_authenticated
              and (request.user.moderator
                   or request.user.admin
                   or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        ) or (request.user.is_authenticated
              and (request.user.moderator
                   or request.user.admin
                   or request.user.is_superuser))


class IsAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.admin
                     or request.user.is_superuser))


class IsModeratorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.moderator)


class IsSuperuserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.superuser
                     and request.user.is_superuser))


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
        ) or (request.user.is_authenticated
              and (request.user.is_staff or request.user.admin))
