from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from reviews.models import Comment, Review
from titles.models import Categorie, Genre, Title
from users.models import ROLES_CHOICES

User = get_user_model()

class GetTitleDefault:
    "Класс для получения значения title_id из контекста."
    requires_context = True

    def __call__(self, serializer):
        return (serializer.context.get('request')
                .parser_context.get('kwargs').get('title_id'))


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        queryset=Title.objects.all(),
        slug_field='id',
        default=GetTitleDefault()
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('author', 'title')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message='У вас уже есть отзыв!'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)


class CategorieSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Categorie."""

    class Meta:
        fields = ('name', 'slug')
        model = Categorie


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ViewsTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели просмотра Title."""
    category = CategorieSerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        read_only_fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class EditTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для редактирования модели Title."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categorie.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')


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
