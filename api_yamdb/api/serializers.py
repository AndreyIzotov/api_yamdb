from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Review, Comment
from title.models import Title


# class TitleSerializer(serializers.ModelSerializer):
#    """Сериализатор для модели Title."""
#    rating = serializers.SerializerMethodField()
#
#    class Meta:
#        model = Title
#        fields = '__all__'

class GetTitleDefault:
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
