from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets, generics, status, permissions
from rest_framework.parsers import MultiPartParser
from .utils import *
from rest_framework.decorators import action
from rest_framework.response import Response
from . import my_generics
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
#new
from django.http import JsonResponse
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
import json
from rest_framework.decorators import api_view


# Create your views here.
class RoleViewSet(viewsets.ViewSet, generics.CreateAPIView, my_generics.ListApiViewFilterByName,
                  my_generics.UpdateAPIView):
    queryset = Role.objects.all().order_by('name')
    serializer_class = RoleSerializer


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, my_generics.ListApiViewFilterByName):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_class = [MultiPartParser, ]

    # permission_classes = [my_permission.KLTNPermissionUser]
    # phân quyền các chức năng
    def get_permissions(self):
        if self.action in ['get_current_user', 'patch_current_user', 'patch_password']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=["patch"], url_path="change-user", detail=False)
    def patch_current_user(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(user, data=request.data, partial=True)

        # Kiểm tra serializer có hợp lệ không
        if serializer.is_valid():
            # Kiểm tra và loại bỏ các trường username và password nếu có
            if 'username' in serializer.validated_data:
                del serializer.validated_data['username']
            if 'password' in serializer.validated_data:
                del serializer.validated_data['password']

            # Lưu thông tin cập nhật
            instance = serializer.save()

            return Response(UserDetailSerializer(instance, context={'request': request}).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], url_path="current-user", detail=False)
    def get_current_user(self, request):
        user = request.user
        return Response(UserDetailSerializer(user, context={"request": request}).data)

    @action(methods=["patch"], url_path="change-password", detail=False)
    def patch_password(self, request):
        user = self.request.user
        old_password = self.request.data.get('old_password')
        new_password = self.request.data.get('new_password')
        if not check_password(old_password, user.password):
            return Response({"detail": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Changed password successfully"}, status=status.HTTP_200_OK)


class GenreViewSet(viewsets.ViewSet, generics.CreateAPIView, my_generics.ListApiViewFilterByName,
                   my_generics.UpdateAPIView):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer


class MovieViewSet(viewsets.ViewSet, generics.CreateAPIView, my_generics.ListApiViewFilterByName,my_generics.UpdateAPIView,generics.RetrieveAPIView):
    queryset = Movie.objects.all().order_by('-created_date')
    serializer_class = MovieSerializer

    def get_serializer_class(self):
        if self.action in ['list']:
            return MovieListSerializer
        if self.action in ['retrieve']:
            return MovieDetailSerializer
        return self.serializer_class

    @action(methods=['post'],url_path='add-genres-to-movie',detail=True)
    def add_genres_to_movie(self, request, pk=None):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found."}, status=status.HTTP_404_NOT_FOUND)

        genre_ids = request.data.get('genre_ids', [])

        # Add selected genres to the movie
        for genre_id in genre_ids:
            try:
                genre = Genre.objects.get(id=genre_id)
                MovieGenre.objects.create(movie=movie, genre=genre)
            except Genre.DoesNotExist:
                pass
            except IntegrityError:
                pass
        return Response({"message": "Adding genres to movie successfully"},status=status.HTTP_200_OK)


class MovieEpisodeViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = MovieEpisode.objects.all()
    serializer_class = MovieEpisodeSerializer


stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            intent = stripe.PaymentIntent.create(
                amount=data['amount'],
                currency='usd',
                payment_method_types=['card'],
            )
            return JsonResponse({'client_secret': intent['client_secret']})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)