from rest_framework import serializers
from .models import MentorshipFeedback
from django.utils import timezone


class MentorshipFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorshipFeedback
        fields = ['id', 'loop', 'user', 'comments', 'submitted_at', 'rate', 'successful']
        read_only_fields = ['id', 'submitted_at', 'user']

    def validate(self, data):
        user = self.context['request'].user
        loop = data['loop']

        if loop.is_active or loop.end_date > timezone.now().date():
            raise serializers.ValidationError("Feedback can only be submitted after the loop ends.")

        if MentorshipFeedback.objects.filter(loop=loop, user=user).exists():
            raise serializers.ValidationError("You have already submitted feedback for this loop.")

        return data



