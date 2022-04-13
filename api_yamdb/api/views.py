from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Review, Title
from titles.models import Categorie, Genre, Title
from users.confirmation_code import generate_confirmation_code
from api.filters import TitlesFilter
from api.permissions import (IsAdminOrReadOnly, IsAdminPermission,
                             IsAuthorOrReadOnly, IsSuperuserPermission)
from api.serializers import (CategorieSerializer, CommentSerializer,
                             EditTitleSerializer, GenreSerializer,
                             MeSerializer, ReviewSerializer,
                             SignUpSerializer, TokenSerializer,
                             UserSerializer, ViewsTitleSerializer)

User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами."""
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_review(self):
        return get_object_or_404(
            Review,
            title_id=self.kwargs.get('title_id'),
            pk=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class BasicForGenreCategorieViewSet(mixins.CreateModelMixin,
                                    mixins.ListModelMixin,
                                    mixins.DestroyModelMixin,
                                    viewsets.GenericViewSet):
    """Базовый вьюсет для работы с категориями и жанрами."""
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(BasicForGenreCategorieViewSet):
    """Вьюсет для работы с жанрами."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(BasicForGenreCategorieViewSet):
    """Вьюсет для работы с категориями."""
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с произведениями."""
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return EditTitleSerializer
        return ViewsTitleSerializer


@api_view(['POST'])
def sign_up(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    try:
        User.objects.get_or_create(
            username=username,
            email=email)
    except IntegrityError:
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
    confirmation_code = generate_confirmation_code()
    User.objects.filter(email=email).update(
        confirmation_code=confirmation_code
    )
    send_mail(
        'Подтверждение регистрации на YaMDB',
        f'Код подтверждения {confirmation_code}',
        settings.FROM_EMAIL,
        [serializer.validated_data['email']],
    )
    return Response(
        {'email': email,
         'username': username},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username'])
    if (user.confirmation_code
       != serializer.validated_data['confirmation_code']):
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
