from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import (
    ReviewViewSet,
    CommentViewSet
)

# Версия роутера
router_V001 = routers.DefaultRouter()

# Регистрация маршрутов
router_V001.register(
    r'titles/(?P<titles_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router_V001.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<reviews_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(router_V001.urls)),
    path('v1/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
