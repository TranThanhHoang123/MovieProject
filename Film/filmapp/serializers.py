from rest_framework import serializers
from .models import Role, User


# SERIALIZERS IN THIS SCOPE USE FOR CREATING AND UPDATING
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'email', 'image', 'role', 'phone_number', 'address','date_of_birth']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(data['password'])
        user.save()
        return user





# SERIALIZERS IN THERE USE FOR DETAIL AND LIST
class UserDetailSerializer(UserSerializer):
    role = RoleSerializer()
    image = serializers.SerializerMethodField(source="image")
    #overwrite image
    def get_image(self, obj):
        if obj.image:
            # Lấy tên file hình ảnh từ đường dẫn được lưu trong trường image
            image_name = obj.image.name
            return self.context['request'].build_absolute_uri(f"/static/{image_name}")
        return None
    class Meta(UserSerializer.Meta):
        pass