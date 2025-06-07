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


                

class WeeklyCheckInUpdateView(generics.RetrieveUpdateAPIView):
    queryset = WeeklyCheckIn.objects.all()
    serializer_class = WeeklyCheckInSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(WeeklyCheckIn, pk=self.kwargs['pk'])

    def perform_update(self, serializer):
        checkin = self.get_object()
        loop = checkin.loop
        user = self.request.user

        if loop.status not in ["ongoing", "completed"]:
            raise PermissionDenied("This mentorship loop is not in a valid state for check-ins.")

        if loop.mentor.user != user and loop.mentee.user != user:
            raise PermissionDenied("You are not a participant in this mentorship loop.")

        instance = serializer.save()

        if instance.status == WeeklyCheckIn.STATUS_COMPLETED:
            send_checkin_completed_email.delay(instance.id)
            if instance.week_number == 4:
                send_loop_completion_email.delay(instance.loop.id)











# Weekly Check-In Submission
class WeeklyCheckInListForBackendView(generics.ListCreateAPIView):
    queryset = WeeklyCheckIn.objects.all()
    serializer_class = WeeklyCheckInSerializer
    permission_classes = [permissions.IsAuthenticated]




    

class WeeklyCheckInUpdateForBackendView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WeeklyCheckInSerializer
    queryset = WeeklyCheckIn.objects.all()

    def get_object(self):
        return get_object_or_404(WeeklyCheckIn, pk=self.kwargs['pk']) # or pk=pk

    def perform_update(self, serializer):
        instance = serializer.save()

        if instance.status == WeeklyCheckIn.STATUS_COMPLETED:
            send_checkin_completed_email.delay(instance.id)

            if instance.week_number == 4:
                send_loop_completion_email.delay(instance.loop.id)


