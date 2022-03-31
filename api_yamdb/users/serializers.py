from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    pass


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all()), ],
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all()), ],
    )

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('"me" is invalid username')
        return value


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=200, required=True)
    verification_code = serializers.CharField(max_length=200, required=True)

    class Meta:
        fields = ('username', 'confirmation_code')

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise exceptions.NotFound(f'There is no user {value}')
        return value
