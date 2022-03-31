from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('role',)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('"me" is invalid username')
        return value


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
        fields = ('username', 'verification_code')
        model = User

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise exceptions.NotFound(f'There is no user {value}')
        return value
