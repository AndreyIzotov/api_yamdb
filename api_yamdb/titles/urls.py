from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router_v1 = SimpleRouter()
router_v1.register(r'categories', views.СategorieViewSet, basename='categorie')
router_v1.register(r'genres', views.GenreViewSet, basename='genre')
router_v1.register(r'titles', views.TitleViewSet, basename='title')
urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
