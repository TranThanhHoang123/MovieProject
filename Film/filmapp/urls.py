from django.urls import path, include
from rest_framework import routers
from . import views
from .views import create_payment
router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user')  # Specify the basename here
router.register(r'role', views.RoleViewSet, basename='role')  # Specify the basename here
router.register(r'genre', views.GenreViewSet, basename='genre')  # Specify the basename here
router.register(r'movie', views.MovieViewSet, basename='movie')  # Specify the basename here
router.register(r'movie-episode', views.MovieEpisodeViewSet, basename='movie-episode')  # Specify the basename here
urlpatterns = [
    path('', include(router.urls)),
    path('create-payment/', create_payment, name='create-payment'),]