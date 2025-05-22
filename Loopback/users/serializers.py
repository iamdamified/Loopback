
from rest_framework import serializers
from .models import User
from profiles.models import MentorProfile, MenteeProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


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
    experience = serializers.IntegerField(required=False, allow_null=True)
    linkedin = serializers.URLField(required=False, allow_blank=True)
    website = serializers.URLField(required=False, allow_blank=True)
    X_account = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'first_name', 'last_name', 'role',
            'passport_image', 'company', 'job_title', 'industry', 'bio',
            'interests', 'goals', 'skills', 'experience', 'linkedin',
            'website', 'X_account'
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
            'experience': validated_data.pop('experience', 0),
            'linkedin': validated_data.pop('linkedin', ''),
            'website': validated_data.pop('website', ''),
            'X_account': validated_data.pop('X_account', '')
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

        return user, profile





# User = get_user_model()


# # USERS INFORMATION SERIALIZERS
# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     role = serializers.ChoiceField(choices=User.ROLE_CHOICES)
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     # Extra profile fields
#     company = serializers.CharField(required=False, allow_blank=True)
#     job_title = serializers.CharField(required=False, allow_blank=True)
#     industry = serializers.CharField(required=False, allow_blank=True)
#     passport_image = serializers.ImageField(required=False)

#     class Meta:
#         model = User
#         fields = [
#             'email', 'password', 'first_name', 'last_name',
#             'role', 'company', 'job_title', 'industry', 'passport_image'
#         ]

#     def create(self, validated_data):
#         role = validated_data.pop('role')
#         password = validated_data.pop('password')
#         validated_data.pop('company', '')
#         validated_data.pop('job_title', '')
#         validated_data.pop('industry', '')
#         validated_data.pop('passport_image', None)

#         user = User.objects.create_user(
#             password=password,
#             role=role,
#             **validated_data
#         )
#         user.is_active = False  # Optional: block login until email is verified
#         user.save()
#         return user
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