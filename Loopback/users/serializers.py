
from rest_framework import serializers
from .models import User
from profiles.models import MentorProfile, MenteeProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer

User = get_user_model()

# This serialiszer is used to manage role-based access control and attributes based control to profile models from user registration.
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    # Extended profile fields
    passport_image = serializers.ImageField(required=False, allow_null=True)
    company = serializers.CharField(required=False, allow_blank=True)
    job_title = serializers.CharField(required=False, allow_blank=True)
    industry = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    interests = serializers.CharField(required=False, allow_blank=True)
    goals = serializers.CharField(required=False, allow_blank=True)
    skills = serializers.CharField(required=False, allow_blank=True)
    experience_years = serializers.IntegerField(required=False, allow_null=True)
    linkedin = serializers.URLField(required=False, allow_blank=True)
    website = serializers.URLField(required=False, allow_blank=True)
    X_account = serializers.CharField(required=False, allow_blank=True)
    expertise = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'first_name', 'last_name', 'role',
            'passport_image', 'company', 'job_title', 'industry', 'bio',
            'interests', 'goals', 'skills', 'experience_years', 'linkedin',
            'website', 'X_account', 'expertise'
        ]

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')

        # Extract shared profile fields
        profile_fields = {
            'passport_image': validated_data.pop('passport_image', None),
            'first_name': validated_data.get('first_name'),
            'last_name': validated_data.get('last_name'),
            'company': validated_data.pop('company', ''),
            'job_title': validated_data.pop('job_title', ''),
            'industry': validated_data.pop('industry', ''),
            'bio': validated_data.pop('bio', ''),
            'interests': validated_data.pop('interests', ''),
            'goals': validated_data.pop('goals', ''),
            'skills': validated_data.pop('skills', ''),
            'experience_years': validated_data.pop('experience_years', 0),
            'linkedin': validated_data.pop('linkedin', ''),
            'website': validated_data.pop('website', ''),
            'X_account': validated_data.pop('X_account', ''),
            'expertise': validated_data.pop('expertise', '')

        }

        # Create the user
        user = User.objects.create_user(
            password=password,
            role=role,
            **validated_data
        )
        user.is_active = False
        user.save()

        # update the profile
        if role == 'mentor':
            profile, _ = MentorProfile.objects.get_or_create(user=user)
        elif role == 'mentee':
            profile, _ = MenteeProfile.objects.get_or_create(user=user)

        for field, value in profile_fields.items():
            setattr(profile, field, value)
        profile.save()

        return user




# GOOGLE OAUTH2 REGISTRATION/LOGIN SERIALIZER
class CustomRegisterSerializer(RegisterSerializer):
    username = None  # remove username field

    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }


# User = get_user_model()



# AUTHENTICATION SERIALIZER FOR LOGIN API
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.verified:
            raise serializers.ValidationError('Please verify your email before logging in.')
        data['user_id'] = self.user.id
        data['role'] = self.user.role
        return data
