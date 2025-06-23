from rest_framework import serializers
from .models import SupportTicket

class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ['id', 'user', 'subject', 'comment', 'response', 'is_resolved', 'created_at', 'responded_at']
        read_only_fields = ['id', 'user', 'response', 'is_resolved', 'created_at', 'responded_at']


class AdminResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ['response', 'is_resolved']
