from django.shortcuts import render
from .serializers import MentorshipFeedbackSerializer
from .models import MentorshipFeedback
from rest_framework import generics, permissions




class SubmitFeedbackView(generics.CreateAPIView):
    queryset = MentorshipFeedback.objects.all()
    serializer_class = MentorshipFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class UserFeedbackListView(generics.ListAPIView):
    serializer_class = MentorshipFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MentorshipFeedback.objects.filter(user=self.request.user)


# Backend Use
class AllFeedbackListView(generics.ListAPIView):
    queryset = MentorshipFeedback.objects.all()
    serializer_class = MentorshipFeedbackSerializer
    permission_classes = [permissions.IsAdminUser]
