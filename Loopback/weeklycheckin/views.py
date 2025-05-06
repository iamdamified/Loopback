from django.shortcuts import render
from .serializers import WeeklycheckinSerializer
from .models import Weeklycheckin
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

# Create your views here.

class WeeklycheckinViewSet(viewsets.ModelViewSet):
    queryset = Weeklycheckin.objects.all()
    serializer_class = WeeklycheckinSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
