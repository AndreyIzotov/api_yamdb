from django.urls import path

from .views import GetTokenAPI, SignUpAPI

urlpatterns = [
    path('v1/auth/signup/', SignUpAPI.as_view(), name='signup'),
    path('v1/auth/token/', GetTokenAPI.as_view(), name='token'),
]
