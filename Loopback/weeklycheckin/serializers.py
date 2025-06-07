from rest_framework import serializers
from .models import WeeklyCheckIn


# # WEEKLY CHECKINS SERIALIZERS


class WeeklyCheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyCheckIn
        fields = [
            'id', 'loop', 'week_number', 'mentor_checked_in', 'mentee_checked_in',
            'progress', 'challenges', 'feedback', 'checkin_date', 'status', 'created_at',
        ]
        read_only_fields = [
            'week_number', 'status', 'created_at',
            'mentor_checked_in', 'mentee_checked_in'
        ]