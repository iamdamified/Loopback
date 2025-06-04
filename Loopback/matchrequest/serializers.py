from rest_framework import serializers
from .models import MatchRequest, MeetingSchedule

class MatchRequestSerializer(serializers.ModelSerializer):
    # mentor_name = serializers.CharField(source="mentor.user.get_full_name", read_only=True)
    # mentee_name = serializers.CharField(source="mentee.user.get_full_name", read_only=True)

    class Meta:
        model = MatchRequest
        fields = ['id', 'mentor', 'mentee', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']


class MeetingScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingSchedule
        fields = '__all__'
        read_only_fields = ['created_at']