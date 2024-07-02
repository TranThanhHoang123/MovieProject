from rest_framework import serializers
from .models import *


# SERIALIZERS IN THIS SCOPE USE FOR CREATING AND UPDATING
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'email', 'image', 'role', 'phone_number', 'address', 'date_of_birth']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(data['password'])
        user.save()
        return user


# thể loại film
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class MovieGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieGenre
        fields = '__all__'


# SERIALIZERS IN THERE USE FOR DETAIL AND LIST
class UserDetailSerializer(UserSerializer):
    role = RoleSerializer()
    image = serializers.SerializerMethodField(source="image")

    # overwrite image
    def get_image(self, obj):
        if obj.image:
            # Lấy tên file hình ảnh từ đường dẫn được lưu trong trường image
            image_name = obj.image.name
            return self.context['request'].build_absolute_uri(f"/static/{image_name}")
        return None

    class Meta(UserSerializer.Meta):
        pass


class MovieDetailSerializer(MovieSerializer):
    poster = serializers.SerializerMethodField(source="poster")

    def get_poster(self, obj):
        if obj.poster:
            # Lấy tên file hình ảnh từ đường dẫn được lưu trong trường image
            poster = obj.poster.name
            return self.context['request'].build_absolute_uri(f"/static/{poster}")
        return None

    class Meta(MovieSerializer.Meta):
        pass


class MovieListSerializer(MovieDetailSerializer):
    class Meta(MovieDetailSerializer.Meta):
        fields = ['id', 'name', 'rating', 'release_date', 'duration', 'poster']
