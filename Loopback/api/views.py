# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .tasks import sync_google_calendar_meetings_for_user

# class GoogleCalendarSyncView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         sync_google_calendar_meetings_for_user.delay(request.user.id)
#         return Response({'status': 'sync started'})
# # Create your views here.







