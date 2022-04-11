from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .confirmation_code import generate_confirmation_code
from .models import User
from .permissions import IsAdminPermission, IsSuperuserPermission
from .serializers import (MeSerializer, SignUpSerializer, TokenSerializer,
                          UserSerializer)


@api_view(['POST'])
def SignUpAPI(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    try:
        User.objects.get(
            username=username,
            email=email)
    except User.DoesNotExist:
        if User.objects.filter(username=username).exists():
            return Response(
                'Такой username уже есть',
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(email=email).exists():
            return Response(
                'Такой email уже есть',
                status=status.HTTP_400_BAD_REQUEST
            )
    User.objects.create(username=username, email=email)
    confirmation_code = generate_confirmation_code()
    User.objects.filter(email=email).update(
        confirmation_code = confirmation_code
    )
    send_mail(
        'Подтверждение регистрации на YaMDB',
        f'Код подтверждения {confirmation_code}',
        settings.FROM_EMAIL,
        [serializer.validated_data['email']],
    )
    return Response(
        {'email': serializer.validated_data['email'],
         'username': serializer.validated_data['username']},
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
def GetTokenAPI(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username'])
    if user.confirmation_code != serializer.validated_data['confirmation_code']:
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

    @action(detail=False, permission_classes=(IsAuthenticated,),
            serializer_class=MeSerializer,
            methods=['get', 'patch'], url_path='me')
    def get_or_update_self(self, request):
        if request.method != 'GET':
            serializer = self.get_serializer(
                instance=request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = self.get_serializer(request.user, many=False)
        return Response(serializer.data)
