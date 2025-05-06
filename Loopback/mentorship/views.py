from django.shortcuts import render
from .models import Mentorship
from users.models import User
from .serializers import MentorshipSerializer
from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return object.mentor == request.user or obj.mentee == request.User
    
class MentorshipViewSet(viewsets.ModelViewSet):
    queryset = Mentorship.objects.all()
    serializer_class = MentorshipSerializer
    permission_classes = [IsAuthenticated, IsParticipant]

    def get_queryset(self):
        user = self.request.user
        return Mentorship.objects.filter(models.Q(mentor=user) | models.Q(mentee=user))
    
    def perform_create(self, serializer):
        serializer.save()