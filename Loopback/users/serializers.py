
from rest_framework import serializers
from .models import User
from profiles.models import MentorProfile, MenteeProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


# USERS INFORMATION SERIALIZERS
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    # Extra profile fields
    company = serializers.CharField(required=False, allow_blank=True)
    job_title = serializers.CharField(required=False, allow_blank=True)
    industry = serializers.CharField(required=False, allow_blank=True)
    passport_image = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'first_name', 'last_name',
            'role', 'company', 'job_title', 'industry', 'passport_image'
        ]

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')
        validated_data.pop('company', '')
        validated_data.pop('job_title', '')
        validated_data.pop('industry', '')
        validated_data.pop('passport_image', None)

        user = User.objects.create_user(
            password=password,
            role=role,
            **validated_data
        )
        user.is_active = False  # Optional: block login until email is verified
        user.save()
        return user
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id','email', 'role', 'first_name', 'last_name', 'verified']



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