from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GetTokenAPI, SignUpAPI, UsersViewSet

router = DefaultRouter()
router.register('users', UsersViewSet)

urlpatterns = [
    path('v1/auth/signup/', SignUpAPI.as_view(), name='signup'),
    path('v1/auth/token/', GetTokenAPI.as_view(), name='token'),
    path('v1/', include(router.urls)),
]
