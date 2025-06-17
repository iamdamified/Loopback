from django.shortcuts import render
from .serializers import WeeklyCheckInSerializer
from .models import WeeklyCheckIn
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.tasks import send_checkin_completed_email, send_loop_completion_email
from rest_framework.exceptions import PermissionDenied
from mentorship.models import MentorshipLoop
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import WeeklyCheckInSerializer
from .models import WeeklyCheckIn
from matchrequest.models import MatchRequest



class GoogleCalendarCheckInCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Optional: Restrict to logged-in users

    def post(self, request, *args, **kwargs):
        data = request.data

        # Expected payload example from frontend:
        # {
        #     "loop": 1, will have field  week_number:1 OR  "match": 1, has no week_number
        #     "google_event_id": "abc123",
        #     "week_number": 2,
        #     "weekly_goals": "Discuss project progress",
        #     "scheduled_date": "2025-06-25",
        #     "start_time": "10:00:00",
        #     "end_time": "11:00:00",
        #     "meetining_link": "https://meet.google.com/xyz-defg"
        # }

        serializer = WeeklyCheckInSerializer(data=data)
        if serializer.is_valid():
            if WeeklyCheckIn.objects.filter(google_event_id=data.get("google_event_id")).exists():
                return Response({"error": "Meeting already exists."}, status=400)
            serializer.save()
            return Response({
                "message": "Check-in meeting successfully scheduled.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# THIS VERSION ENFORCES ALL CONTROL FOR THE CHECKINS CREATION

# class GoogleCalendarCheckInCreateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         data = request.data
#         user = request.user

#         loop_id = data.get("loop")
#         match_id = data.get("match")

#         # Enforce that either loop or match is provided
#         if not loop_id and not match_id:
#             return Response(
#                 {"error": "Either 'loop' or 'match' must be provided."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # If loop is provided, check if the user is the mentor
#         if loop_id:
#             try:
#                 loop = MentorshipLoop.objects.get(id=loop_id)
#                 if loop.mentor != user:
#                     return Response(
#                         {"error": "You are not authorized to schedule meetings for this loop."},
#                         status=status.HTTP_403_FORBIDDEN
#                     )
#             except MentorshipLoop.DoesNotExist:
#                 return Response(
#                     {"error": "MentorshipLoop not found."},
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#         # If match is provided, check if user is either mentor or mentee
#         if match_id:
#             try:
#                 match = MatchRequest.objects.get(id=match_id)
#                 if match.mentor != user and match.mentee != user:
#                     return Response(
#                         {"error": "You are not authorized to schedule meetings for this match."},
#                         status=status.HTTP_403_FORBIDDEN
#                     )
#             except MatchRequest.DoesNotExist:
#                 return Response(
#                     {"error": "MatchRequest not found."},
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#         # If passed all checks, continue
#         serializer = WeeklyCheckInSerializer(data=data)
#         if serializer.is_valid():
#             if WeeklyCheckIn.objects.filter(google_event_id=data.get("google_event_id")).exists():
#                 return Response({"error": "Meeting already exists."}, status=400)
#             serializer.save()
#             return Response({
#                 "message": "Check-in meeting successfully scheduled.",
#                 "data": serializer.data
#             }, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from .models import WeeklyCheckInFeedback
from .serializers import WeeklyCheckInFeedbackSerializer

class WeeklyCheckInFeedback(generics.CreateAPIView, generics.UpdateAPIView):
    # POST to create, PUT/PATCH to update check-in feedback
    serializer_class = WeeklyCheckInFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]  # Optional: adjust as needed

    def get_queryset(self):
        return WeeklyCheckInFeedback.objects.all()

    def get_object(self):
        loop_id = self.request.data.get('loop')
        week_number = self.request.data.get('week_number')
        return WeeklyCheckInFeedback.objects.get(loop_id=loop_id, week_number=week_number)
    



class WeeklyCheckInListCreateView(generics.ListCreateAPIView):
    serializer_class = WeeklyCheckInSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return WeeklyCheckIn.objects.filter(
            loop__mentor__user=user
        ) | WeeklyCheckIn.objects.filter(
            loop__mentee__user=user
        )

    def perform_create(self, serializer):
        user = self.request.user
        loop = serializer.validated_data.get("loop")

        if loop.status not in ["ongoing", "completed"]:
            raise PermissionDenied("You can only check into loops that are ongoing or completed.")

        if loop.mentor.user != user and loop.mentee.user != user:
            raise PermissionDenied("You are not part of this mentorship loop.")

        current_week_count = WeeklyCheckIn.objects.filter(loop=loop).count()
        instance = serializer.save(week_number=current_week_count + 1)

        if instance.status == WeeklyCheckIn.STATUS_COMPLETED:
            send_checkin_completed_email.delay(instance.id)
            if instance.week_number == 4:
                send_loop_completion_email.delay(instance.loop.id)


                

# class WeeklyCheckInUpdateView(generics.RetrieveUpdateAPIView):
#     queryset = WeeklyCheckIn.objects.all()
#     serializer_class = WeeklyCheckInSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         return get_object_or_404(WeeklyCheckIn, pk=self.kwargs['pk'])

#     def perform_update(self, serializer):
#         checkin = self.get_object()
#         loop = checkin.loop
#         user = self.request.user

#         if loop.status not in ["ongoing", "completed"]:
#             raise PermissionDenied("This mentorship loop is not in a valid state for check-ins.")

#         if loop.mentor.user != user and loop.mentee.user != user:
#             raise PermissionDenied("You are not a participant in this mentorship loop.")

#         instance = serializer.save()

#         if instance.status == WeeklyCheckIn.STATUS_COMPLETED:
#             send_checkin_completed_email.delay(instance.id)
#             if instance.week_number == 4:
#                 send_loop_completion_email.delay(instance.loop.id)











# Weekly Check-In Submission
# class WeeklyCheckInListForBackendView(generics.ListCreateAPIView):
#     queryset = WeeklyCheckIn.objects.all()
#     serializer_class = WeeklyCheckInSerializer
#     permission_classes = [permissions.IsAuthenticated]




    

# class WeeklyCheckInUpdateForBackendView(generics.RetrieveUpdateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = WeeklyCheckInSerializer
#     queryset = WeeklyCheckIn.objects.all()

#     def get_object(self):
#         return get_object_or_404(WeeklyCheckIn, pk=self.kwargs['pk']) # or pk=pk

#     def perform_update(self, serializer):
#         instance = serializer.save()

#         if instance.status == WeeklyCheckIn.STATUS_COMPLETED:
#             send_checkin_completed_email.delay(instance.id)

#             if instance.week_number == 4:
#                 send_loop_completion_email.delay(instance.loop.id)


