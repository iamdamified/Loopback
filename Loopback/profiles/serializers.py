from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import MentorProfile, MenteeProfile
from users.serializers import UserRegistrationSerializer

User = get_user_model()


# Mentor Profile Serializer
class MentorProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)

    class Meta:
        model = MentorProfile
        fields = [
            'id', 'passport_image', 'first_name', 'last_name',
            'company', 'job_title', 'industry', 'bio', 'interests', 'goals',
            'skills', 'experience_years', 'linkedin', 'website', 'X_account'
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        # Update user fields
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance




# Mentee Profile Serializer
class MenteeProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)

    class Meta:
        model = MenteeProfile
        fields = [
            'id', 'passport_image', 'first_name', 'last_name',
            'company', 'job_title', 'industry', 'bio', 'interests', 'goals',
            'skills', 'experience_years', 'linkedin', 'website', 'X_account'
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        # Update user fields
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
