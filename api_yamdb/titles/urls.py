from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import GenreViewSet, TitleViewSet, СategorieViewSet

router_v1 = SimpleRouter()
router_v1.register('categories', СategorieViewSet, basename='categorie')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('titles', TitleViewSet, basename='title')
urlpatterns = [
    path('v1/', include(router_v1.urls)),
]

