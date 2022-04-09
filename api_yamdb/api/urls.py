from django.urls import include, path
from rest_framework import routers

from api.views import CommentViewSet, ReviewViewSet

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

urlpatterns = [
    path('v1/', include(router_V001.urls)),
]
