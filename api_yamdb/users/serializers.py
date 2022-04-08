from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator

from .models import ROLES_CHOICES, User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(
            queryset=User.objects.all()), ],)
    username = serializers.CharField(
        required=True, validators=[UniqueValidator(
            queryset=User.objects.all()), ],)
    role = serializers.ChoiceField(required=False,
                                   choices=ROLES_CHOICES)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('"me" не допустимый юзернейм')
        return value


class MeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(
            queryset=User.objects.all()), ],)
    username = serializers.CharField(
        required=True, validators=[UniqueValidator(
            queryset=User.objects.all()), ],)
    role = serializers.ChoiceField(required=False,
                                   choices=ROLES_CHOICES,
                                   read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('"me" не допустимый юзернейм')
        return value


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all()), ],
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all()), ],
    )

    class Meta:
        fields = ('username', 'email',)
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('"me" не допустимый юзернейм')
        return value


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=200, required=True)
    confirmation_code = serializers.CharField(max_length=200, required=True)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise exceptions.NotFound(f'Нет такого пользователя {value}')
        return value
