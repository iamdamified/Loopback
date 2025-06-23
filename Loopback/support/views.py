from django.shortcuts import render
from rest_framework import generics, permissions
from .models import SupportTicket
from .serializers import SupportTicketSerializer, AdminResponseSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.utils import timezone

class CreateSupportTicketView(generics.CreateAPIView):
    serializer_class = SupportTicketSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListUserSupportTicketsView(generics.ListAPIView):
    serializer_class = SupportTicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SupportTicket.objects.filter(user=self.request.user)


class AdminSupportTicketListView(generics.ListAPIView):
    queryset = SupportTicket.objects.all().order_by('-created_at')
    serializer_class = SupportTicketSerializer
    permission_classes = [IsAdminUser]


class AdminRespondToTicketView(generics.UpdateAPIView):
    queryset = SupportTicket.objects.all()
    serializer_class = AdminResponseSerializer
    permission_classes = [IsAdminUser]

    def perform_update(self, serializer):
        serializer.save(responded_at=timezone.now())

