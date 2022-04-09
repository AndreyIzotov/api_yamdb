from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters


from .filters import TitlesFilter
from .permissions import IsAdminPermission, MainPermission
from .models import Categorie, Genre, Title
from .serializers import CategorieSerializer, GenreSerializer
from .serializers import ViewsTitleSerializer, EditTitleSerializer


class BasicForGenreСategorieViewSet(mixins.CreateModelMixin,
                                    mixins.ListModelMixin,
                                    mixins.DestroyModelMixin,
                                    viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated, IsAdminPermission)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'

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

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter
    permission_classes = [MainPermission] 

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return EditTitleSerializer
        return ViewsTitleSerializer
