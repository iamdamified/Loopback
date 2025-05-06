from django.shortcuts import render
from users.models import User
from mentorship.models import Mentorship
from matchrequest.models import MatchRequest
from .models import Profile, Interest, Skill
from rest_framework.generics import CreateAPIView,ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView
from .serializers import ProfileSerializer, InterestSerializer, SkillSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions, status, viewsets
from api.matching import search_mentor_for_mentee
# Create your views here.


# Users Profile Retrieval and Update

class ProfileUserUpdateView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    
    def perform_update(self, serializer):
        profile = serializer.save()

        # Only run matching logic if profile is being updated to mentee (you can refine this)
        if profile.role == 'mentee' and not Mentorship.objects.filter(mentee=profile).exists():
            matched_mentor = search_mentor_for_mentee(profile)
            if matched_mentor:
                # MatchRequest.objects.get_or_create OR Mentorship.objects.create
                MatchRequest.objects.get_or_create(
                    mentor=matched_mentor,
                    mentee=profile,
                    is_active=True,
                )
        return Response({'message': 'MatchRequest created: mentee {profile.user.username} → mentor {matched_mentor.user.username}'}, status=201)
        # return Response(f"MatchRequest created: mentee {profile.user.username} → mentor {matched_mentor.user.username}")
    









# Backend Profile Creation and Operations
class ProfileUserCreate(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    lookup_field = "id"

class ProfileUserUpdate(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    lookup_field = "id"




# Backend Dynamic Use for Matching Only.
class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer