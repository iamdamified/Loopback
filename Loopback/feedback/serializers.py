from rest_framework import serializers
from .models import LoopFeedback


class LoopFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoopFeedback
        fields = '__all__'
        read_only_fields = ['created_by', 'created']