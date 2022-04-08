from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination

from .models import Categorie, Genre, Title
from .serializers import CategorieSerializer, GenreSerializer, TitleListSerializer, TitleSerializerPost


class BasicForGenreСategorieViewSet(mixins.CreateModelMixin,
                                    mixins.ListModelMixin,
                                    mixins.DestroyModelMixin,
                                    viewsets.GenericViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class GenreViewSet(BasicForGenreСategorieViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class СategorieViewSet(BasicForGenreСategorieViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer


#class TitleViewSet(viewsets.ModelViewSet):
#    queryset = Title.objects.all()
#    pagination_class = LimitOffsetPagination
#    serializer_class = TitleSerializer
class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleSerializerPost
        return TitleListSerializer
