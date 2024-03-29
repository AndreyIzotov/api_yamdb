from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

from users.managers import UserManager


class UserRole:
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    SUPERUSER = 'superuser'


ROLES_CHOICES = [
    (UserRole.USER, 'user'),
    (UserRole.MODERATOR, 'moderator'),
    (UserRole.ADMIN, 'admin'),
    (UserRole.SUPERUSER, 'superuser'),
]


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель User с собственными полями"""

    username_validator = RegexValidator(r'^[\w.@+-]+')

    username = models.CharField(max_length=150,
                                blank=True,
                                null=True,
                                default='None',
                                verbose_name='Юзернейм',
                                validators=[username_validator],
                                unique=True,
                                )

    bio = models.TextField(
        null=True,
        verbose_name='Биография',
    )

    confirmation_code = models.CharField(
        max_length=100,
        null=True,
        verbose_name='Код подтверждения',
    )

    role = models.CharField(
        max_length=max(len(role) for role, _ in ROLES_CHOICES),
        choices=ROLES_CHOICES,
        default=UserRole.USER,
        verbose_name='Роль',
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Почта',
    )

    first_name = models.CharField(max_length=150,
                                  blank=True,
                                  null=True,
                                  verbose_name='Имя',
                                  )

    last_name = models.CharField(max_length=150,
                                 blank=True,
                                 null=True,
                                 verbose_name='Фамилия',
                                 )

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    @property
    def admin(self):
        return self.role == UserRole.ADMIN or (
            self.is_admin or self.is_staff
        )

    @property
    def superuser(self):
        return self.role == UserRole.SUPERUSER or self.is_admin

    @property
    def moderator(self):
        return self.role == UserRole.MODERATOR or self.is_staff

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = UserManager()

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self
