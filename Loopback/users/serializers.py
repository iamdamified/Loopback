from .models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# USERS INFORMATION SERIALIZERS
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name', 'verified']



# AUTHENTICATION SERIALIZER FOR API
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.verified:
            raise serializers.ValidationError('Please verify your email before logging in.')
        data['user_id'] = self.user.id
        data['role'] = self.user.role
        return data

# class ProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)

#     class Meta:
#         model = Profile
#         fields = ['user', 'bio', 'interests', 'goals', 'skills', 'experience']