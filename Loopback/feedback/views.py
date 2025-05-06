from django.shortcuts import render
from .serializers import LoopFeedbackSerializer
from .models import LoopFeedback
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class LoopFeedbackViewSet(viewsets.ModelViewSet):
    queryset = LoopFeedback.objects.all()
    serializer_class = LoopFeedbackSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)