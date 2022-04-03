from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .serializers import SignUpSerializer, TokenSerializer


class SignUpAPI(APIView):
    """Запрос на регистрацию"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            raise ValidationError('invalid data')
        user, was_created = User.objects.get_or_create(
            email=serializer.data['email'],
            username=serializer.data['username'],
        )
        if not was_created:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Подтверждение регистрации на YaMDB',
            f'Код подтверждения {confirmation_code}',
            settings.FROM_EMAIL,
            [serializer.data['email']],
        )
        return Response(
            {'email': serializer.data['email'],
             'username': serializer.data['username']},
            status=status.HTTP_200_OK
        )


class GetTokenAPI(APIView):
    """Запрос на получение токена"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            raise ValidationError('invalid data')
        user = get_object_or_404(
            User, username=serializer.data['username'])
        if not default_token_generator.check_token(
                user, serializer.data['confirmation_code']):
            return Response(
                {'confirmation_code': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST
            )
        access_token = AccessToken.for_user(user)
        return Response(
            {'token': str(access_token)}, status=status.HTTP_200_OK
        )
