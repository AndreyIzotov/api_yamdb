from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import IsAdminPermission, IsSuperuserPermission
from .serializers import SignUpSerializer, TokenSerializer, UserSerializer


class SignUpAPI(APIView):
    """Запрос на регистрацию"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            raise ValidationError('invalid data')
        User.objects.get_or_create(
            email=serializer.data['email'],
            username=serializer.data['username'],
        )
        email = serializer.data['email']
        confirmation_code = (
            User.objects.filter(email=email).first().confirmation_code
        )
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
        if user.confirmation_code != serializer.data['confirmation_code']:
            return Response(
                {'confirmation_code': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST
            )
        access_token = AccessToken.for_user(user)
        return Response(
            {'token': str(access_token)}, status=status.HTTP_200_OK
        )


class UsersViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    search_fields = ("user__username",)
    permission_classes = (IsAuthenticated,
                          IsAdminPermission | IsSuperuserPermission)
    pagination_class = LimitOffsetPagination

    @action(detail=False, permission_classes=(IsAuthenticated,),
            serializer_class=UserSerializer,
            methods=['get', 'patch', 'delete'], url_path='me')
    def get_or_update_self(self, request):
        if request.method != 'GET':
            serializer = self.get_serializer(
                instance=request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(request.user, many=False)
            return Response(serializer.data)
