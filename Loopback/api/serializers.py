from users.models import User, Profile, Interest, Skill, Mentorship, Goal, Weeklycheckin, LoopFeedback
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer




# USERS INFORMATION SERIALIZERS
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name', 'verified']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'interests', 'goals', 'skills', 'experience']



# For Backend Dynamic input Only.
class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']


# AUTHENTICATION SERIALIZER FOR API
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.verified:
            raise serializers.ValidationError('Please verify your email before logging in.')
        data['user_id'] = self.user.id
        data['role'] = self.user.role
        return data


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
        
#         data['role'] = self.user.role
#         return data





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





