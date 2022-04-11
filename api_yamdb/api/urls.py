from django.urls import include, path
from rest_framework import routers

from api.views import (CommentViewSet, ReviewViewSet, CategoryViewSet,
                       GenreViewSet, TitleViewSet)

# Версия роутера
router_V001 = routers.DefaultRouter()

# Регистрация маршрутов
router_V001.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router_V001.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
router_V001.register('categories', CategoryViewSet, basename='categorie')
router_V001.register('genres', GenreViewSet, basename='genre')
router_V001.register('titles', TitleViewSet, basename='title')

urlpatterns = [
    path('v1/', include(router_V001.urls)),
]
