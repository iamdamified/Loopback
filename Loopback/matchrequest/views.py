from django.shortcuts import render
from .models import MatchRequest
from .serializers import MatchRequestSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from mentorship.models import Mentorship

# Create your views here.

class MatchRequestViewSet(viewsets.ModelViewSet):
    queryset = MatchRequest.objects.all()
    serializer_class = MatchRequestSerializer

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        match_request = self.get_object()
        if match_request.mentor.user != request.user:
            return Response({'error': 'Not authorized.'}, status=403)

        match_request.is_approved = True
        match_request.responded = True
        match_request.save()

        Mentorship.objects.create(
            mentor=match_request.mentor,
            mentee=match_request.mentee,
            is_active=True,
        )

        return Response({'status': 'Match approved and mentorship loop started.'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        match_request = self.get_object()
        if match_request.mentor.user != request.user:
            return Response({'error': 'Not authorized.'}, status=403)

        match_request.responded = True
        match_request.save()

        return Response({'status': 'Match not accepted, please, view suggestions and update your profile'})
    

