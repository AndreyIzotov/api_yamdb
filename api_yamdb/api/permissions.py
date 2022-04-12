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
        ) or (request.user.is_authenticated and (request.user.role in (
            'moderator', 'admin', 'superuser')))

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        ) or (request.user.is_authenticated and (request.user.role in (
            'moderator', 'admin', 'superuser')))


class IsAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.admin
                     or request.user.is_superuser))


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.admin
