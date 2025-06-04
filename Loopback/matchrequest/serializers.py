from rest_framework import serializers
from .models import MatchRequest, MeetingSchedule

class MatchRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchRequest
        fields = ['id', 'mentor', 'mentee', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']


class MeetingScheduleSerializer(serializers.ModelSerializer):
    scheduled_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    class Meta:
        model = MeetingSchedule
        fields = ['id', 'scheduled_time', 'comment', 'meetining_link', 'created_at']
        read_only_fields = ['created_at']