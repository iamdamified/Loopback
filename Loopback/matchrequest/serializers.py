from rest_framework import serializers
from .models import MatchRequest

class MatchRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchRequest
        fields = '__all__'
        read_only_fields = ['status', 'created_at']