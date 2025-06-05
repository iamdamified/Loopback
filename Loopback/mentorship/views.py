from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import MentorshipLoop
from .serializers import MentorshipLoopSerializer
from profiles.models import MentorProfile, MenteeProfile
from matchrequest.models import MatchRequest

class CreateMentorshipLoopView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        mentor = get_object_or_404(MentorProfile, user=request.user)
        mentee_id = request.data.get("mentee_id")
        purpose = request.data.get("purpose")

        if not mentee_id:
            return Response({"detail": "Mentee ID is required."}, status=400)

        try:
            mentee = MenteeProfile.objects.get(id=mentee_id)
        except MenteeProfile.DoesNotExist:
            return Response({"detail": "Mentee not found."}, status=404)

        # Parse start_date if provided
        start_date_str = request.data.get("start_date")
        if start_date_str:
            try:
                start_date = timezone.datetime.strptime(start_date_str, "%Y-%m-%d").date()
                if start_date < timezone.now().date():
                    return Response({"detail": "Start date cannot be in the past."}, status=400)
            except ValueError:
                return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=400)
        else:
            start_date = timezone.now().date()

        end_date = start_date + timedelta(weeks=4)

        # Check for max active loops
        active_loops = MentorshipLoop.objects.filter(mentor=mentor, is_active=True).count()
        if active_loops >= 5:
            return Response({"detail": "You already have 5 active mentorship loops."}, status=400)

        # Check for completed match request
        match_request = MatchRequest.objects.filter(mentor=mentor, mentee=mentee, status='completed').first()
        if not match_request:
            return Response({"detail": "You must have a completed match request with this mentee."}, status=400)

        # Check if meeting has been scheduled
        if not match_request.schedules.exists():
            return Response({"detail": "You must have scheduled a meeting with this mentee before creating a loop."}, status=400)

        # Prevent duplicate loop
        if MentorshipLoop.objects.filter(mentor=mentor, mentee=mentee, is_active=True).exists():
            return Response({"detail": "You already have an active mentorship loop with this mentee."}, status=400)

        # Create loop
        mentorship_loop = MentorshipLoop.objects.create(
            mentor=mentor,
            mentee=mentee,
            purpose=purpose,
            start_date=start_date,
            end_date=end_date,
            status='pending',
            is_active=True
        )


        send_mail(
            subject='🎉 Your Mentorship Loop Has Been Created!',
            message=f"""
        Hi {mentee.user.first_name},

        A new mentorship loop has been initiated by your mentor {mentor.user.first_name} {mentor.user.last_name}.

        📝 Purpose: {purpose or 'No purpose provided'}
        📅 Start Date: {start_date}
        📅 End Date: {end_date}

        Please be prepared and make the most of your upcoming sessions!

        Best,
        The Mentorship Team
        """.strip(),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[mentee.user.email],
            fail_silently=False  
        )

        serializer = MentorshipLoopSerializer(mentorship_loop)
        return Response(serializer.data, status=201)

# class MentorshipLoopViewSet(viewsets.ModelViewSet):
#     queryset = MentorshipLoop.objects.all()
#     serializer_class = MentorshipLoopSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         if hasattr(user, 'mentor_profile'):
#             return MentorshipLoop.objects.filter(mentor=user.mentor_profile)
#         elif hasattr(user, 'mentee_profile'):
#             return MentorshipLoop.objects.filter(mentee=user.mentee_profile)
#         return MentorshipLoop.objects.none()

#     def perform_create(self, serializer):
#         mentor = serializer.validated_data['mentor']
#         mentee = serializer.validated_data['mentee']
        
#         # Prevent multiple active loops between the same mentor and mentee
#         if MentorshipLoop.objects.filter(mentor=mentor, mentee=mentee, is_active=True).exists():
#             raise serializers.ValidationError("An active mentorship loop already exists between this mentor and mentee.")

#         serializer.save()

#     @action(detail=True, methods=['post'], url_path='deactivate')
#     def deactivate_loop(self, request, pk=None):
#         loop = self.get_object()
#         loop.is_active = False
#         loop.save()
#         return Response({'detail': 'Loop deactivated.'}, status=status.HTTP_200_OK)

#     @action(detail=False, methods=['post'], url_path='auto-create')
#     def auto_create_from_match(self, request):
#         match_id = request.data.get('match_id')
#         match = get_object_or_404(MatchRequest, id=match_id, status='accepted')

#         # Prevent duplicates
#         if MentorshipLoop.objects.filter(mentor=match.mentor, mentee=match.mentee, is_active=True).exists():
#             return Response({"detail": "An active loop already exists for this match."}, status=status.HTTP_400_BAD_REQUEST)

#         loop = MentorshipLoop.objects.create(mentor=match.mentor, mentee=match.mentee)
#         serializer = self.get_serializer(loop)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)






# MENTORSHIP USERS FRONTEND DASHBOARD VIEWS (I WILL CREATE A SEPARATE APP FOR THIS AFTER MOVING FILES)


# class DashboardView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         is_mentor = hasattr(user, 'mentor_profile')
#         is_mentee = hasattr(user, 'mentee_profile')

#         match_requests = MatchRequest.objects.filter(
#             mentor__user=user if is_mentor else None,
#             mentee__user=user if is_mentee else None
#         )

#         loops = MentorshipLoop.objects.filter(
#             mentor__user=user if is_mentor else None,
#             mentee__user=user if is_mentee else None
#         )

#         pending_requests = match_requests.filter(status='pending')
#         active_loops = loops.filter(is_active=True)
#         completed_loops = loops.filter(is_active=False)

#         return Response({
#             "profile_type": "mentor" if is_mentor else "mentee",
#             "pending_requests": DashboardMatchRequestSerializer(pending_requests, many=True).data,
#             "active_loops": DashboardLoopSerializer(active_loops, many=True, context={'request': request}).data,
#             "completed_loops": DashboardLoopSerializer(completed_loops, many=True, context={'request': request}).data
#         })
