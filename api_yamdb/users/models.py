from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель User с собственными полями"""

    ROLES_CHOICES = [
        (settings.USER, 'user'),
        (settings.MODERATOR, 'moderator'),
        (settings.ADMIN, 'admin'),
    ]

    username = models.CharField(max_length=50,
                                blank=True,
                                null=True,
                                default='None',
                                verbose_name='Юзернейм',
                                )

    bio = models.CharField(
        max_length=1000,
        null=True,
        verbose_name='Биография',
    )

    verification_code = models.CharField(
        max_length=100,
        null=True,
        verbose_name='Код подтверждения',
    )

    role = models.CharField(
        max_length=50,
        choices=ROLES_CHOICES,
        default=settings.USER,
        verbose_name='Роль',
    )

    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name='Почта',
    )

    first_name = models.CharField(max_length=40,
                                  blank=True,
                                  null=True,
                                  verbose_name='Имя',
                                  )

    last_name = models.CharField(max_length=40,
                                 blank=True,
                                 null=True,
                                 verbose_name='Фамилия',
                                 )

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = UserManager()

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self
