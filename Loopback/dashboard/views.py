from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from mentorship.models import MenteeProfile, MentorshipLoop
from matchrequest.models import MeetingSchedule
from weeklycheckin.models import WeeklyCheckIn
from .serializers import MenteeDashboardSerializer, MentorDashboardSerializer, MenteeInfoSerializer, MentorInfoSerializer, MeetingScheduleSerializer, WeeklyCheckInSerializer


class MenteeDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            mentee_profile = user.mentee_profile
        except MenteeProfile.DoesNotExist:
            return Response({'error': 'Mentee profile not found.'}, status=404)

        current_loop = MentorshipLoop.objects.filter(mentee=mentee_profile, is_active=True).order_by('-created_at').first()
        if not current_loop:
            return Response({'error': 'No active mentorship loop found.'}, status=404)

        mentor = current_loop.mentor
        last_schedule = MeetingSchedule.objects.filter(match_request__mentee=mentee_profile).order_by('-created_at').first()
        completed_checkins = WeeklyCheckIn.objects.filter(
            loop=current_loop, mentee_checked_in=True, status=WeeklyCheckIn.STATUS_COMPLETED
        ).order_by('week_number')
        pending_checkins = WeeklyCheckIn.objects.filter(
            loop=current_loop, mentee_checked_in=False, status=WeeklyCheckIn.STATUS_PENDING
        ).order_by('week_number')

        # Pass objects as instance dict, not .data!
        dashboard_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "current_loop_status": current_loop.status,
            "mentor": mentor,
            "last_weekly_goals": last_schedule,
            "completed_checkins": completed_checkins,
            "pending_checkins": pending_checkins,
        }

        serializer = MenteeDashboardSerializer(dashboard_data)
        return Response(serializer.data)
    

class MentorDashboardView(APIView):
    pass