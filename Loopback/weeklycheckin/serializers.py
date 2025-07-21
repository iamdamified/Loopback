from rest_framework import serializers
from .models import WeeklyCheckIn, WeeklyCheckInFeedback
from mentorship.models import MentorshipLoop
from matchrequest.models import MatchRequest


class WeeklyCheckInSerializer(serializers.ModelSerializer):
    is_completed = serializers.ReadOnlyField()
    loop = serializers.PrimaryKeyRelatedField(
        queryset=MentorshipLoop.objects.all(),
        required=False,
        allow_null=True
    )
    match = serializers.PrimaryKeyRelatedField(
        queryset=MatchRequest.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = WeeklyCheckIn
        fields = [
            'id', 'loop', 'match', 'google_event_id', 'week_number', 'weekly_goals', 'scheduled_date',
            'start_time', 'end_time', 'meetining_link', 'created_at', 'updated_at', 'status', 'checkin_created', 'is_completed'
        ]
        read_only_fields = ['created_at', 'updated_at', 'status', 'checkin_created', 'is_completed']

    def validate(self, data):
        if not data.get('loop') and not data.get('match'):
            raise serializers.ValidationError("Either 'loop' or 'match' must be provided.")
        return data




class WeeklyCheckInFeedbackSerializer(serializers.ModelSerializer):
    loop = serializers.PrimaryKeyRelatedField(queryset=MentorshipLoop.objects.all())

    class Meta:
        model = WeeklyCheckInFeedback
        fields = [
            'id', 'loop', 'week_number', 'mentor_checked_in', 'mentee_checked_in',
            'progress', 'challenges', 'feedback', 'checkin_date', 'status', 'created_at',
        ]
        read_only_fields = ['status', 'created_at']

    def validate_week_number(self, value):
        if not 1 <= value <= 4:
            raise serializers.ValidationError("Week number must be between 1 and 4.")
        return value

    def validate(self, data):
        loop = data.get('loop')
        week_number = data.get('week_number')

        if self.instance is None and WeeklyCheckInFeedback.objects.filter(loop=loop, week_number=week_number).exists():
            raise serializers.ValidationError("Feedback for this loop and week already exists.")
        return data