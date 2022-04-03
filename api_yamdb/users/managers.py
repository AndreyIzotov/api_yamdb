from django.conf import settings
from django.contrib.auth.models import UserManager


class UserManager(UserManager):
    """Менеджер пользователей"""
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Требуется Email')
        if username == 'me':
            raise ValueError('"me" не допустимый юзернейм')
        return super().create_user(
            username, email=email, password=password, **extra_fields)

    def create_superuser(
            self, username, email, password, role, **extra_fields):
        return super().create_superuser(
            username, email, password, role=settings.ADMIN, **extra_fields)
