from rest_framework import serializers
from .models import MatchRequest


# Match Rrequest to Matched Mentor
class MatchRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchRequest
        fields = ['id', 'mentor', 'mentee', 'created_at', 'is_approved', 'responded']

