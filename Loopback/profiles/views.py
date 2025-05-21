# Create your views here.
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .matching import get_suggested_mentors_for_mentee
from rest_framework import generics, permissions, status, viewsets
from .models import MentorProfile, MenteeProfile
from .serializers import MentorProfileSerializer, MenteeProfileSerializer



# Get current user's Mentor Profile
class MentorProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = MentorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return MentorProfile.objects.get(user=self.request.user)

# Get current user's Mentee Profile

class MenteeProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = MenteeProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return MenteeProfile.objects.get(user=self.request.user)
    
    # I intend to add suggestion logic from matching.py here to be activated upon profile creation