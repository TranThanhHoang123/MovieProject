from django.urls import path, include
from rest_framework import routers
from . import views
router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user')  # Specify the basename here
router.register(r'role', views.RoleViewSet, basename='role')  # Specify the basename here
urlpatterns = [
    path('', include(router.urls)),
]