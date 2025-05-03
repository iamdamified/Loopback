from users.models import User, Profile, Interest, Skill
from mentorship.models import MatchRequest, Mentorship, Goal
from weeklycheckin.models import Weeklycheckin
from feedback.models import LoopFeedback
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



class ProfileSerializer(serializers.ModelSerializer):
    interests = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Interest.objects.all()
    )
    skills = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Skill.objects.all()
    )

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'role', 'goals', 'interests', 'skills',
        ]
        read_only_fields = ['user']

    def create(self, validated_data):
        interests = validated_data.pop('interests', [])
        skills = validated_data.pop('skills', [])
        profile = Profile.objects.create(**validated_data)

        profile.interests.set(interests)
        profile.skills.set(skills)
        return profile

    def update(self, instance, validated_data):
        interests = validated_data.pop('interests', None)
        skills = validated_data.pop('skills', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if interests is not None:
            instance.interests.set(interests)

        if skills is not None:
            instance.skills.set(skills)

        instance.save()
        return instance


# For Backend Dynamic input Only.
class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']


# Match Rrequest to Matched Mentor
class MatchRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchRequest
        fields = ['id', 'mentor', 'mentee', 'created_at', 'is_approved', 'responded']


# LOOP SERIALIZERS

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        models = Goal
        fields = '__all__'
        read_only_fields = ['created_by']


class MentorshipSerializer(serializers.ModelSerializer):
    goals = GoalSerializer(many=True, read_only=True)

    class Meta:
        model = Mentorship
        fields = '__all__'
        read_only_fields = ['status']















# WEEKLY CHECKINS SERIALIZERS
class WeeklycheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weeklycheckin
        fields = '__all__'
        read_only_fields = ['created_by', 'created']





class LoopFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoopFeedback
        fields = '__all__'
        read_only_fields = ['created_by', 'created']





