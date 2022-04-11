from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator

from .models import ROLES_CHOICES, User


class ValidateUsernameSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('"me" не допустимый юзернейм')
        return value


class UserSerializer(ValidateUsernameSerializer):
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


class MeSerializer(ValidateUsernameSerializer):
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


class SignUpSerializer(ValidateUsernameSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('username', 'email',)
        model = User


class TokenSerializer(ValidateUsernameSerializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=200, required=True)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User
