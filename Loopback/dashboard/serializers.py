from rest_framework import serializers
from profiles.models import MenteeProfile, MentorProfile
from mentorship.models import MentorshipLoop
from weeklycheckin.models import WeeklyCheckIn



class MentorInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = MentorProfile
        fields = [
            'first_name', 'last_name', 'passport_image', 'bio', 'experience_years'
        ]

class WeeklyCheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyCheckIn
        fields = ['weekly_goals', 'scheduled_date', 'start_time', 'meetining_link']

class WeeklyCheckInDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyCheckIn
        fields = [
            'id', 'loop', 'match', 'google_event_id', 'week_number', 'weekly_goals', 'scheduled_date',
            'start_time', 'end_time', 'meetining_link', 'created_at', 'updated_at', 'status'
        ]

class MenteeDashboardSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    current_loop_status = serializers.CharField()
    mentor = MentorInfoSerializer()
    last_weekly_goals = WeeklyCheckInSerializer(allow_null=True)
    completed_checkins = WeeklyCheckInDetailSerializer(many=True)
    pending_checkins = WeeklyCheckInDetailSerializer(many=True)



class MentorDashboardSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    current_loop_status = serializers.CharField()
    last_weekly_goals = WeeklyCheckInSerializer(allow_null=True)
    completed_checkins = WeeklyCheckInDetailSerializer(many=True)
    next_checkin = WeeklyCheckInDetailSerializer(allow_null=True)
    next_meeting = WeeklyCheckInSerializer(allow_null=True)