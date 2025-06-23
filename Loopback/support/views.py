from django.shortcuts import render
from rest_framework import generics, permissions
from .models import SupportTicket
from .serializers import SupportTicketSerializer, AdminResponseSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status

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
        ticket = serializer.save(responded_at=timezone.now())

        # Send email notification to user
        send_mail(
            subject=f"Response to Your Support Ticket: {ticket.subject}",
            message=f"Hello {ticket.user.first_name},\n\nYour support ticket has been updated:\n\n{ticket.admin_response}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[ticket.user.email],
            fail_silently=False,
        )