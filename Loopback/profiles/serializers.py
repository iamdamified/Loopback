from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import MentorProfile, MenteeProfile
from users.serializers import UserRegistrationSerializer

User = get_user_model()


# Mentor Profile Serializer
class MentorProfileSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer(read_only=True)

    class Meta:
        model = MentorProfile
        fields = [
            'id', 'user', 'passport_image', 'first_name', 'last_name', 'company', 'job_title',
            'industry', 'bio', 'interests', 'goals', 'skills', 'experience',
            'linkedin', 'website', 'X_account'
        ]

# Mentee Profile Serializer
class MenteeProfileSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer(read_only=True)

    class Meta:
        model = MenteeProfile
        fields = [
            'id', 'user', 'passport_image', 'first_name', 'last_name', 'company', 'job_title',
            'industry', 'bio', 'interests', 'goals', 'skills', 'experience',
            'linkedin', 'website', 'X_account'
        ]
