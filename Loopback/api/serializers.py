from users.models import User, Profile
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# AUTHENTICATION SERIALIZER FOR API
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'interests', 'goals', 'skills', 'experience']