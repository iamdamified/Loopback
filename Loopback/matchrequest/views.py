from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from profiles.models import MenteeProfile, MentorProfile
from matchrequest.models import MatchRequest
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from .serializers import MatchRequestSerializer
from mentorship.models import MentorshipLoop
from datetime import timedelta
from django.utils import timezone



User = get_user_model()

class MatchRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        mentee = MenteeProfile.objects.get(user=request.user)
        mentor_id = request.data.get("mentor_id")
        mentor = get_object_or_404(MentorProfile, id=mentor_id)

        # Abort if the mentee has a pending or accepted match request
        existing_request = MatchRequest.objects.filter(
            mentee=mentee,
            status__in=["pending", "accepted"]
        ).first()
        if existing_request:
            return Response({"detail": "You already have a pending or accepted match request."}, status=400)

        # Abort if the mentor already has 5 pending or accepted requests
        mentor_active_requests = MatchRequest.objects.filter(
            mentor=mentor,
            status__in=["pending", "accepted"]
        ).count()
        if mentor_active_requests >= 5:
            return Response({"detail": "This mentor already has 5 pending or accepted match requests."}, status=400)

        # Create match request
        match_request, created = MatchRequest.objects.get_or_create(
            mentor=mentor, mentee=mentee, defaults={"status": "pending"}
        )
        if not created:
            return Response({"detail": "Match request already exists."}, status=400)

        # Send email to mentor
        send_mail(
            subject="New Mentorship Match Request",
            message=(
                f"{mentee.user.first_name} {mentee.user.last_name} has requested to start a mentorship loop with you on LoopBack. "
                "Please login to accept or decline."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[mentor.user.email]
        )

        return Response({"detail": "Match request sent to mentor."})
    



class MatchResponseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, match_request_id):
        match_request = get_object_or_404(MatchRequest, id=match_request_id, mentor__user=request.user)
        decision = request.data.get("decision")

        if decision not in ["accept", "decline"]:
            return Response({"error": "Decision must be 'accept' or 'decline'."}, status=400)

        if decision == "accept":
            match_request.status = "accepted"
            match_request.save()

            send_mail(
                subject="Mentorship Request Accepted",
                message=f"{match_request.mentor.user.first_name} {match_request.mentor.user.last_name} has accepted your mentorship request. You will receive further instructions from your mentor soon",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[match_request.mentee.user.email]
            )
            
        else:
            match_request.status = "declined"
            match_request.save()

            send_mail(
                subject="Mentorship Request Declined",
                message=f"Unfortunately, {match_request.mentor.first_name} {match_request.mentor.last_name} has declined your mentorship request.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[match_request.mentee.user.email]
            )

        return Response({"detail": f"Match request {decision}ed."})


class MentorMatchesRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            mentor_profile = MentorProfile.objects.get(user=request.user)
        except MentorProfile.DoesNotExist:
            return Response({"detail": "Mentor profile not found."}, status=404)

        match_requests = MatchRequest.objects.filter(mentor=mentor_profile)
        serializer = MatchRequestSerializer(match_requests, many=True)
        return Response(serializer.data)


class MenteeMatchesRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            mentee_profile = MenteeProfile.objects.get(user=request.user)
        except MenteeProfile.DoesNotExist:
            return Response({"detail": "Mentee profile not found."}, status=404)

        match_requests = MatchRequest.objects.filter(mentee=mentee_profile)
        serializer = MatchRequestSerializer(match_requests, many=True)
        return Response(serializer.data)