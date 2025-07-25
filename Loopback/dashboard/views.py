from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from mentorship.models import MenteeProfile, MentorProfile, MentorshipLoop
# from matchrequest.models import MeetingSchedule
from weeklycheckin.models import WeeklyCheckIn
from .serializers import MenteeDashboardSerializer, MentorDashboardSerializer, WeeklyCheckInSerializer, MentorInfoSerializer, WeeklyCheckInSerializer
from django.utils import timezone
from django.db.models import Q


## NEW VIEWS TO COMPARE AND IMPLEMENT

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
        last_schedule = WeeklyCheckIn.objects.filter(match__mentee=mentee_profile).order_by('-created_at').first()

        completed_checkins = WeeklyCheckIn.objects.filter(
            loop=current_loop, status=WeeklyCheckIn.STATUS_COMPLETED
        ).order_by('week_number')

        pending_checkins = WeeklyCheckIn.objects.filter(
            loop=current_loop, status=WeeklyCheckIn.STATUS_PENDING
        ).order_by('week_number')

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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            mentor_profile = user.mentor_profile
        except MentorProfile.DoesNotExist:
            return Response({'error': 'Mentor profile not found.'}, status=404)

        loops = MentorshipLoop.objects.filter(mentor=mentor_profile)
        if loops.filter(status='ongoing').exists():
            current_loop_status = 'ongoing'
        else:
            current_loop_status = 'pending'

        last_schedule = WeeklyCheckIn.objects.filter(
            match__mentor=mentor_profile
        ).order_by('-created_at').first()

        completed_checkins = WeeklyCheckIn.objects.filter(
            loop__mentor=mentor_profile, status=WeeklyCheckIn.STATUS_COMPLETED
        ).order_by('scheduled_date')

        next_checkin = WeeklyCheckIn.objects.filter(
            loop__mentor=mentor_profile,
            status=WeeklyCheckIn.STATUS_PENDING,
            scheduled_date__gte=timezone.now().date()
        ).order_by('scheduled_date').first()

        next_meeting = WeeklyCheckIn.objects.filter(
            match__mentor=mentor_profile,
            scheduled_date__gte=timezone.now().date()
        ).order_by('scheduled_date').first()

        dashboard_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "current_loop_status": current_loop_status,
            "last_weekly_goals": last_schedule,
            "completed_checkins": completed_checkins,
            "next_checkin": next_checkin,
            "next_meeting": next_meeting,
        }

        serializer = MentorDashboardSerializer(dashboard_data)
        return Response(serializer.data)
    


    
# class MenteeDashboardView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         try:
#             mentee_profile = user.mentee_profile
#         except MenteeProfile.DoesNotExist:
#             return Response({'error': 'Mentee profile not found.'}, status=404)

#         current_loop = MentorshipLoop.objects.filter(mentee=mentee_profile, is_active=True).order_by('-created_at').first()
#         if not current_loop:
#             return Response({'error': 'No active mentorship loop found.'}, status=404)

#         mentor = current_loop.mentor
#         last_schedule = WeeklyCheckIn.objects.filter(match_request__mentee=mentee_profile).order_by('-created_at').first()
#         # To let display only last weekly_goal field
#         # last_weekly_goals = (
#         #     MeetingSchedule.objects
#         #     .filter(match_request__mentor=mentor_profile)
#         #     .order_by('-created_at')
#         #     .values_list('weekly_goals', flat=True)
#         #     .first()
#         # )
#         completed_checkins = WeeklyCheckIn.objects.filter(
#             # loop=current_loop, mentee_checked_in=True, status=WeeklyCheckIn.STATUS_COMPLETED
#             loop=current_loop, status=WeeklyCheckIn.STATUS_COMPLETED
#         ).order_by('week_number')
#         pending_checkins = WeeklyCheckIn.objects.filter(
#             # loop=current_loop, mentee_checked_in=False, status=WeeklyCheckIn.STATUS_PENDING
#             loop=current_loop, status=WeeklyCheckIn.STATUS_PENDING
#         ).order_by('week_number')

#         # Pass objects as instance dict, not .data!
#         dashboard_data = {
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "current_loop_status": current_loop.status,
#             "mentor": mentor,
#             "last_weekly_goals": last_schedule,
#             "completed_checkins": completed_checkins,
#             "pending_checkins": pending_checkins,
#         }

#         serializer = MenteeDashboardSerializer(dashboard_data)
#         return Response(serializer.data)
    


# class MentorDashboardView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         try:
#             mentor_profile = user.mentor_profile
#         except MentorProfile.DoesNotExist:
#             return Response({'error': 'Mentor profile not found.'}, status=404)

#         # Get all mentorship loops for this mentor
#         loops = MentorshipLoop.objects.filter(mentor=mentor_profile)
#         # Check if any ongoing
#         if loops.filter(status='ongoing').exists():
#             current_loop_status = 'ongoing'
#         else:
#             current_loop_status = 'pending'  # Or whatever your default should be

#         # Last created meeting schedule
#         last_schedule = WeeklyCheckIn.objects.filter(
#             match_request__mentor=mentor_profile
#         ).order_by('-created_at').first()

#         # To let display only last weekly_goal field
#         # last_weekly_goals = (
#         #     MeetingSchedule.objects
#         #     .filter(match_request__mentor=mentor_profile)
#         #     .order_by('-created_at')
#         #     .values_list('weekly_goals', flat=True)
#         #     .first()
#         # )

#         # Completed WeeklyCheckIn (where mentor has checked in and status is completed)
#         completed_checkins = WeeklyCheckIn.objects.filter(
#             # loop__mentor=mentor_profile, mentor_checked_in=True, status=WeeklyCheckIn.STATUS_COMPLETED
#             loop__mentor=mentor_profile, status=WeeklyCheckIn.STATUS_COMPLETED
#         ).order_by('checkin_date')

#         # Next WeeklyCheckIn (pending for mentor, earliest by checkin_date)
#         next_checkin = WeeklyCheckIn.objects.filter(
#             loop__mentor=mentor_profile, status=WeeklyCheckIn.STATUS_PENDING, checkin_date__gte=timezone.now().date()
#         ).order_by('checkin_date').first()

#         # Next MeetingSchedule (future meetings, earliest by scheduled_time)
#         next_meeting = WeeklyCheckIn.objects.filter(
#             match_request__mentor=mentor_profile, scheduled_time__gte=timezone.now()
#         ).order_by('scheduled_time').first()

#         dashboard_data = {
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "current_loop_status": current_loop_status,
#             "last_weekly_goals": last_schedule, #last_weekly_goals
#             "completed_checkins": completed_checkins,
#             "next_checkin": next_checkin,
#             "next_meeting": next_meeting,
#         }

#         serializer = MentorDashboardSerializer(dashboard_data)
#         return Response(serializer.data)


## NEW VIEWS TO COMPARE AND IMPLEMENT

# class MenteeDashboardView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         try:
#             mentee_profile = user.mentee_profile
#         except MenteeProfile.DoesNotExist:
#             return Response({'error': 'Mentee profile not found.'}, status=404)

#         current_loop = MentorshipLoop.objects.filter(mentee=mentee_profile, is_active=True).order_by('-created_at').first()
#         if not current_loop:
#             return Response({'error': 'No active mentorship loop found.'}, status=404)

#         mentor = current_loop.mentor
#         last_schedule = WeeklyCheckIn.objects.filter(match__mentee=mentee_profile).order_by('-created_at').first()

#         completed_checkins = WeeklyCheckIn.objects.filter(
#             loop=current_loop, status=WeeklyCheckIn.STATUS_COMPLETED
#         ).order_by('week_number')

#         pending_checkins = WeeklyCheckIn.objects.filter(
#             loop=current_loop, status=WeeklyCheckIn.STATUS_PENDING
#         ).order_by('week_number')

#         dashboard_data = {
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "current_loop_status": current_loop.status,
#             "mentor": mentor,
#             "last_weekly_goals": last_schedule,
#             "completed_checkins": completed_checkins,
#             "pending_checkins": pending_checkins,
#         }

#         serializer = MenteeDashboardSerializer(dashboard_data)
#         return Response(serializer.data)


# class MentorDashboardView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         try:
#             mentor_profile = user.mentor_profile
#         except MentorProfile.DoesNotExist:
#             return Response({'error': 'Mentor profile not found.'}, status=404)

#         loops = MentorshipLoop.objects.filter(mentor=mentor_profile)
#         if loops.filter(status='ongoing').exists():
#             current_loop_status = 'ongoing'
#         else:
#             current_loop_status = 'pending'

#         last_schedule = WeeklyCheckIn.objects.filter(
#             match__mentor=mentor_profile
#         ).order_by('-created_at').first()

#         completed_checkins = WeeklyCheckIn.objects.filter(
#             loop__mentor=mentor_profile, status=WeeklyCheckIn.STATUS_COMPLETED
#         ).order_by('scheduled_date')

#         next_checkin = WeeklyCheckIn.objects.filter(
#             loop__mentor=mentor_profile,
#             status=WeeklyCheckIn.STATUS_PENDING,
#             scheduled_date__gte=timezone.now().date()
#         ).order_by('scheduled_date').first()

#         next_meeting = WeeklyCheckIn.objects.filter(
#             match__mentor=mentor_profile,
#             scheduled_date__gte=timezone.now().date()
#         ).order_by('scheduled_date').first()

#         dashboard_data = {
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "current_loop_status": current_loop_status,
#             "last_weekly_goals": last_schedule,
#             "completed_checkins": completed_checkins,
#             "next_checkin": next_checkin,
#             "next_meeting": next_meeting,
#         }

#         serializer = MentorDashboardSerializer(dashboard_data)
#         return Response(serializer.data)
