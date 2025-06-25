from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import MentorProfile, MenteeProfile
from users.serializers import UserRegistrationSerializer, download_image_from_url

User = get_user_model()


# Mentor Profile Serializer
class MentorProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)

    class Meta:
        model = MentorProfile
        fields = [
            'id', 'username', 'passport_image', 'passport_image_url', 'first_name', 'last_name',
            'company', 'job_title', 'industry', 'bio', 'interests', 'goals',
            'skills', 'experience_years', 'linkedin', 'website', 'X_account', 'expertise', 'is_available',
            'address', 'phone_number', 'state', 'country', 'google_credentials'
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        # Handle image logic
        passport_image = validated_data.pop('passport_image', None)
        passport_image_url = validated_data.pop('passport_image_url', None)

        if not passport_image and passport_image_url:
            downloaded_image = download_image_from_url(passport_image_url)
            if downloaded_image:
                instance.passport_image = downloaded_image

        elif passport_image:
            instance.passport_image = passport_image

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
            'id', 'username', 'passport_image', 'passport_image_url', 'first_name', 'last_name',
            'company', 'job_title', 'industry', 'bio', 'interests', 'goals',
            'skills', 'experience_years', 'linkedin', 'website', 'X_account', 'expertise', 'is_available',
            'address', 'phone_number', 'state', 'country', 'google_credentials'
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        # Handle image logic
        passport_image = validated_data.pop('passport_image', None)
        passport_image_url = validated_data.pop('passport_image_url', None)

        if not passport_image and passport_image_url:
            downloaded_image = download_image_from_url(passport_image_url)
            if downloaded_image:
                instance.passport_image = downloaded_image

        elif passport_image:
            instance.passport_image = passport_image

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


class MenteeSummarySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = MenteeProfile
        fields = ['id', 'passport_image', 'full_name', 'bio', 'email']

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"


class MentorSummarySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = MentorProfile
        fields = ['id', 'passport_image', 'full_name', 'bio', 'email']

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    


class SuggestedMentorsSerializer(serializers.Serializer):
    mentor = MentorSummarySerializer()
    score = serializers.IntegerField()