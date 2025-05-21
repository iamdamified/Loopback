from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from profiles.models import MenteeProfile, MentorProfile
from matchrequest.models import MatchRequest
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
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

        match_request, created = MatchRequest.objects.get_or_create(
            mentor=mentor, mentee=mentee
        )
        if not created:
            return Response({"detail": "Match request already sent."}, status=400)

        # Send email to mentor
        send_mail(
                subject="New Mentorship Match Request",
                message=f"{mentee.first_name} {mentee.last_name} has requested to start a mentorship loop with you on LoopBack. Please login to accept or decline.",
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

            MentorshipLoop.objects.create(
                mentor=match_request.mentor,
                mentee=match_request.mentee,
                start_date=timezone.now(),
                end_date=timezone.now() + timedelta(weeks=4),
                is_active=True
            )

            send_mail(
                subject="Mentorship Request Accepted",
                message=f"{match_request.mentor.first_name} {match_request.mentor.last_name} has accepted your mentorship request. Your 4-week loop has started!",
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
