from rest_framework import serializers

from .models import User, UserRole


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    roles = UserRoleSerializer(required=False, read_only=True, many=True)

    class Meta:
        model = User
        fields = ["username", "email", "name", "roles"]


class ChangePasswordSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=6)

    class Meta:
        fields = ['new_password', 'old_password']
