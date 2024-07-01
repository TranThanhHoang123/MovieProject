from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets, generics, status, permissions
from rest_framework.parsers import MultiPartParser
from .utils import *
from rest_framework.decorators import action
from rest_framework.response import Response
from . import my_generics
# Create your views here.
class RoleViewSet(viewsets.ViewSet,generics.CreateAPIView,my_generics.ListApiViewSearchByName):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class UserViewSet(viewsets.ViewSet,generics.CreateAPIView,my_generics.ListApiViewSearchByName):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_class = [MultiPartParser,]
    # permission_classes = [my_permission.KLTNPermissionUser]
    #phân quyền các chức năng
    def get_permissions(self):
        if self.action in ['get_current_user','patch_current_user']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]
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

            return Response(UserDetailSerializer(instance,context={'request':request}).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], url_path="current-user", detail=False)
    def get_current_user(self, request):
        user = request.user
        return Response(UserDetailSerializer(user,context={"request": request}).data)