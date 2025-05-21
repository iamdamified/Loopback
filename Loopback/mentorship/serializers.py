from rest_framework import serializers
from .models import MentorshipLoop





class MentorshipLoopSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorshipLoop
        fields = '__all__'
        read_only_fields = ['start_date', 'end_date']




# DASHBOARD SERIALIZERS
from .models import MentorshipLoop
from feedback.models import MentorshipFeedback
from profiles.models import MentorProfile, MenteeProfile
from matchrequest.models import MatchRequest
from users.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers





# MENTORSHIP USERS FRONTEND DASHBOARD (I WILL CREATE A SEPARATE APP FOR THIS AFTER MOVING FILES)
class DashboardMatchRequestSerializer(serializers.ModelSerializer):
    mentor_name = serializers.SerializerMethodField()
    mentee_name = serializers.SerializerMethodField()

    class Meta:
        model = MatchRequest
        fields = ['id', 'mentor', 'mentor_name', 'mentee', 'mentee_name', 'status', 'created_at']

    def get_mentor_name(self, obj):
        return obj.mentor.user.get_full_name()

    def get_mentee_name(self, obj):
        return obj.mentee.user.get_full_name()
    


class DashboardLoopSerializer(serializers.ModelSerializer):
    mentor_name = serializers.SerializerMethodField()
    mentee_name = serializers.SerializerMethodField()
    feedback_submitted = serializers.SerializerMethodField()

    class Meta:
        model = MentorshipLoop
        fields = ['id', 'mentor', 'mentor_name', 'mentee', 'mentee_name',
                  'start_date', 'end_date', 'is_active', 'feedback_submitted']

    def get_mentor_name(self, obj):
        return obj.mentor.user.get_full_name()

    def get_mentee_name(self, obj):
        return obj.mentee.user.get_full_name()

    def get_feedback_submitted(self, obj):
        user = self.context['request'].user
        return MentorshipFeedback.objects.filter(loop=obj, user=user).exists()



