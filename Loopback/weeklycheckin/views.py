from django.shortcuts import render
from .serializers import WeeklyCheckInSerializer
from .models import WeeklyCheckIn
from rest_framework import generics, permissions


# # Create your views here.




# Weekly Check-In Submission
class WeeklyCheckInCreateView(generics.CreateAPIView):
    queryset = WeeklyCheckIn.objects.all()
    serializer_class = WeeklyCheckInSerializer
    permission_classes = [permissions.IsAuthenticated]


