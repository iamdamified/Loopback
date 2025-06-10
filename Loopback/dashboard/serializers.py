from rest_framework import serializers
from profiles.models import MenteeProfile, MentorProfile
from mentorship.models import MentorshipLoop
from matchrequest.models import MeetingSchedule
from weeklycheckin.models import WeeklyCheckIn



class MentorInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = MentorProfile
        fields = [
            'first_name', 'last_name', 'passport_image', 'bio', 'experience_years'
        ]

class MeetingScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingSchedule
        fields = ['weekly_goals', 'scheduled_time', 'meetining_link']

class WeeklyCheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyCheckIn
        fields = [
            'id', 'week_number', 'mentor_checked_in', 'mentee_checked_in', 'progress',
            'challenges', 'feedback', 'checkin_date', 'status', 'created_at'
        ]

class MenteeDashboardSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    current_loop_status = serializers.CharField()
    mentor = MentorInfoSerializer()
    last_weekly_goals = MeetingScheduleSerializer(allow_null=True)
    completed_checkins = WeeklyCheckInSerializer(many=True)
    pending_checkins = WeeklyCheckInSerializer(many=True)