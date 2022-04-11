from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Review, Comment
from titles.models import Categorie, Genre, Title


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
