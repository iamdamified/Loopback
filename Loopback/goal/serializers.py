from rest_framework import serializers
from .models import Goal

# LOOP SERIALIZERS

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        models = Goal
        fields = '__all__'
        read_only_fields = ['created_by']

