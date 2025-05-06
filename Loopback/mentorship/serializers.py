from rest_framework import serializers
from .models import Mentorship
from goal.serializers import GoalSerializer


class MentorshipSerializer(serializers.ModelSerializer):
    goals = GoalSerializer(many=True, read_only=True)

    class Meta:
        model = Mentorship
        fields = '__all__'
        read_only_fields = ['status']