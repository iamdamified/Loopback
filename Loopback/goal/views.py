from django.shortcuts import render
from .serializers import GoalSerializer
from goal.models import Goal
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(loop_mentor=self.request.user) | Goal.objects.filter(loop_mentee=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# Create your views here.
