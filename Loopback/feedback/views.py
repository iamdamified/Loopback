from django.shortcuts import render
from .serializers import MentorshipFeedbackSerializer
from .models import MentorshipFeedback
from rest_framework import generics, permissions

# # Create your views here.

# # Submit Feedback at the End of the Loop
# class LoopFeedbackCreateView(generics.CreateAPIView):
#     queryset = LoopFeedback.objects.all()
#     serializer_class = LoopFeedbackSerializer
#     permission_classes = [permissions.IsAuthenticated]


class SubmitFeedbackView(generics.CreateAPIView):
    queryset = MentorshipFeedback.objects.all()
    serializer_class = MentorshipFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
