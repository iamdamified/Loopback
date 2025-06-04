# Create your views here.
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .matching import get_suggested_mentors_for_mentee
from rest_framework import generics, permissions, filters, status, viewsets
from .models import MentorProfile, MenteeProfile
from .serializers import MentorProfileSerializer, MenteeProfileSerializer, MenteeSummarySerializer, MentorSummarySerializer, SuggestedMentorsSerializer



# Get current user's Mentor Profile
class MentorProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = MentorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return MentorProfile.objects.get(user=self.request.user)

# Get current user's Mentee Profile
class MenteeProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = MenteeProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return MenteeProfile.objects.get(user=self.request.user)

    
    # I intend to add suggestion logic from matching.py here to be activated upon profile creation


class AllMenteesListView(generics.ListAPIView):
    queryset = MenteeProfile.objects.filter(user__verified=True)
    serializer_class = MenteeSummarySerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'bio', 'interests', 'skills', 'industry', 'job_title']
    ordering_fields = ['user__first_name', 'user__last_name', 'created_at']
    ordering = ['user__first_name']  # Default ordering


class MenteeDetailView(generics.RetrieveAPIView):
    queryset = MenteeProfile.objects.filter(user__verified=True)
    serializer_class = MenteeProfileSerializer
    lookup_field = 'id'

    


class AllMentorsListView(generics.ListAPIView):
    queryset = MentorProfile.objects.filter(user__verified=True)
    serializer_class = MentorSummarySerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'bio', 'interests', 'skills', 'industry', 'job_title']
    ordering_fields = ['user__first_name', 'user__last_name', 'created_at']
    ordering = ['user__first_name']



# class SuggestedMentorsListView(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         try:
#             mentee_profile = MenteeProfile.objects.get(user=request.user)
#         except MenteeProfile.DoesNotExist:
#             return Response({"detail": "Mentee profile not found."}, status=404)

#         suggested_mentors = get_suggested_mentors_for_mentee(mentee_profile)
#         serializer = MentorSummarySerializer(suggested_mentors, many=True)

#         return Response(serializer.data)

class SuggestedMentorsListView(generics.ListAPIView):
    serializer_class = SuggestedMentorsSerializer #MentorSummarySerializer #MentorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__first_name', 'user__last_name', 'interests', 'goals']
    ordering_fields = ['user__first_name', 'user__last_name']

    def get_queryset(self):
        try:
            mentee_profile = MenteeProfile.objects.get(user=self.request.user)
        except MenteeProfile.DoesNotExist:
            return MentorProfile.objects.none()

        return get_suggested_mentors_for_mentee(mentee_profile)



class MentorDetailView(generics.RetrieveAPIView):
    queryset = MentorProfile.objects.filter(user__verified=True)
    serializer_class = MentorProfileSerializer
    lookup_field = 'id'


