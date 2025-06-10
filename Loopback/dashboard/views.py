from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from mentorship.models import MenteeProfile, MentorshipLoop
from matchrequest.models import MeetingSchedule
from weeklycheckin.models import WeeklyCheckIn
from .serializers import MenteeDashboardSerializer, MentorInfoSerializer, MeetingScheduleSerializer, WeeklyCheckInSerializer

class MenteeDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            mentee_profile = user.mentee_profile
        except MenteeProfile.DoesNotExist:
            return Response({'error': 'Mentee profile not found.'}, status=404)

        # Current active mentorship loop
        current_loop = MentorshipLoop.objects.filter(mentee=mentee_profile, is_active=True).order_by('-created_at').first()
        if not current_loop:
            return Response({'error': 'No active mentorship loop found.'}, status=404)

        # Mentor Info
        mentor = current_loop.mentor

        # Last created meeting schedule weekly goals
        last_schedule = MeetingSchedule.objects.filter(match_request__mentee=mentee_profile).order_by('-created_at').first()

        # Completed WeeklyCheckIn
        completed_checkins = WeeklyCheckIn.objects.filter(
            loop=current_loop, mentee_checked_in=True, status=WeeklyCheckIn.STATUS_COMPLETED
        ).order_by('week_number')

        # Pending WeeklyCheckIn (pending for mentee)
        pending_checkins = WeeklyCheckIn.objects.filter(
            loop=current_loop, mentee_checked_in=False, status=WeeklyCheckIn.STATUS_PENDING
        ).order_by('week_number')

        # Compose data
        data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "current_loop_status": current_loop.status,
            "mentor": MentorInfoSerializer(mentor).data,
            "last_weekly_goals": MeetingScheduleSerializer(last_schedule).data if last_schedule else None,
            "completed_checkins": WeeklyCheckInSerializer(completed_checkins, many=True).data,
            "pending_checkins": WeeklyCheckInSerializer(pending_checkins, many=True).data,
        }
        return Response(MenteeDashboardSerializer(data).data)
