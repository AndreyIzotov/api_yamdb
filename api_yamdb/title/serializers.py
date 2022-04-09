# from typing_extensions import Required
from django.db.models import Avg
from rest_framework import serializers

from .models import Categorie, Genre, Title, GenreTitle


class CategorieSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name', 'slug']
        model = Categorie


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Genre
        fields = ['name', 'slug']


class GenreTitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = GenreTitle
        fields = ['name', 'slug']


class TitleListSerializer(serializers.ModelSerializer):
    category = CategorieSerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score')).get('score__avg')

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializerPost(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categorie.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category')

    # def create(self, validated_data):
    #    genres = validated_data.pop('genre')
    #    title = Title.objects.create(**validated_data)
    #    for genre in genres:
    #        current_genre, status = Genre.objects.get_or_create(
    #            **genre)
    #        GenreTitle.objects.create(
    #            genre=current_genre, title=title)
    #    return title
