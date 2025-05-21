from django.shortcuts import render
from rest_framework import serializers
from .serializers import MentorshipLoopSerializer
from .models import MentorshipLoop
from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from profiles.models import MentorProfile, MenteeProfile
from matchrequest.models import MatchRequest
from django.shortcuts import get_object_or_404

class MentorshipLoopViewSet(viewsets.ModelViewSet):
    queryset = MentorshipLoop.objects.all()
    serializer_class = MentorshipLoopSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'mentor_profile'):
            return MentorshipLoop.objects.filter(mentor=user.mentor_profile)
        elif hasattr(user, 'mentee_profile'):
            return MentorshipLoop.objects.filter(mentee=user.mentee_profile)
        return MentorshipLoop.objects.none()

    def perform_create(self, serializer):
        mentor = serializer.validated_data['mentor']
        mentee = serializer.validated_data['mentee']
        
        # Prevent multiple active loops between the same mentor and mentee
        if MentorshipLoop.objects.filter(mentor=mentor, mentee=mentee, is_active=True).exists():
            raise serializers.ValidationError("An active mentorship loop already exists between this mentor and mentee.")

        serializer.save()

    @action(detail=True, methods=['post'], url_path='deactivate')
    def deactivate_loop(self, request, pk=None):
        loop = self.get_object()
        loop.is_active = False
        loop.save()
        return Response({'detail': 'Loop deactivated.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='auto-create')
    def auto_create_from_match(self, request):
        match_id = request.data.get('match_id')
        match = get_object_or_404(MatchRequest, id=match_id, status='accepted')

        # Prevent duplicates
        if MentorshipLoop.objects.filter(mentor=match.mentor, mentee=match.mentee, is_active=True).exists():
            return Response({"detail": "An active loop already exists for this match."}, status=status.HTTP_400_BAD_REQUEST)

        loop = MentorshipLoop.objects.create(mentor=match.mentor, mentee=match.mentee)
        serializer = self.get_serializer(loop)
        return Response(serializer.data, status=status.HTTP_201_CREATED)






# MENTORSHIP USERS FRONTEND DASHBOARD VIEWS (I WILL CREATE A SEPARATE APP FOR THIS AFTER MOVING FILES)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from matchrequest.models import MatchRequest
from .models import MentorshipLoop
from .serializers import DashboardMatchRequestSerializer, DashboardLoopSerializer

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        is_mentor = hasattr(user, 'mentor_profile')
        is_mentee = hasattr(user, 'mentee_profile')

        match_requests = MatchRequest.objects.filter(
            mentor__user=user if is_mentor else None,
            mentee__user=user if is_mentee else None
        )

        loops = MentorshipLoop.objects.filter(
            mentor__user=user if is_mentor else None,
            mentee__user=user if is_mentee else None
        )

        pending_requests = match_requests.filter(status='pending')
        active_loops = loops.filter(is_active=True)
        completed_loops = loops.filter(is_active=False)

        return Response({
            "profile_type": "mentor" if is_mentor else "mentee",
            "pending_requests": DashboardMatchRequestSerializer(pending_requests, many=True).data,
            "active_loops": DashboardLoopSerializer(active_loops, many=True, context={'request': request}).data,
            "completed_loops": DashboardLoopSerializer(completed_loops, many=True, context={'request': request}).data
        })
