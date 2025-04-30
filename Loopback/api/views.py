from django.shortcuts import render, redirect
from users.models import User, Profile, Interest, Skill, MatchRequest, Mentorship, Goal, Weeklycheckin, LoopFeedback
from .serializers import UserSerializer, ProfileSerializer, MatchRequestSerializer, InterestSerializer, SkillSerializer, CustomTokenObtainPairSerializer, GoalSerializer, MentorshipSerializer, WeeklycheckinSerializer, LoopFeedbackSerializer
from rest_framework.generics import CreateAPIView,ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView

from .matching import search_mentor_for_mentee

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.hashers import make_password


@login_required
def complete_role(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        if role:
            request.user.role = role
            request.user.save()
            return redirect('home')  # Or dashboard page
    return render(request, 'complete_roles.html')


# Social login view
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        user = request.user
        if user.is_authenticated and not user.role:
            return redirect('complete_role')

        return response



# class CustomTokenView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer


User = get_user_model()

# User Registrations and Access
# class RegisterView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             refresh = RefreshToken.for_user(user)
#             return Response(
#                 {"refresh": str(refresh), "access": str(refresh.access_token)},
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# User Registrations with Verification
class RegisterView(APIView):
    def post(self, request):
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        role = request.data.get('role', 'mentee')

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, role=role)
        user.is_active = False  # Block login until verification
        user.save()

        token = default_token_generator.make_token(user)
        uid = user.pk

        verify_url = f"http://localhost:8000/api/auth/verify-email/{uid}/{token}/"

        send_mail(
            subject="Verify your Email",
            message=f"Click to verify your account: {verify_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )

        return Response({'message': 'Registration successful! Check your email to verify your account.'}, status=201)

# Verification of Email
class VerifyEmailView(APIView):
    def get(self, request, uid, token):
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response({'error': 'Invalid user'}, status=400)

        if default_token_generator.check_token(user, token):
            user.verified = True
            user.is_active = True
            user.save()
            return Response({'message': 'Email verified! You can now log in.'}, status=200)

        return Response({'error': 'Invalid or expired token'}, status=400)
    

# LOG IN
class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = self.user  # Make sure to access authenticated user

        if user and not user.role:
            raise AuthenticationFailed('Please complete your profile by selecting a role.')

        return response


class LoginView(APIView):
    def post(self, request):
        from django.contrib.auth import authenticate
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if not user.role:
                return Response({"error": "Please complete your profile by selecting a role."}, status=status.HTTP_403_FORBIDDEN)

            refresh = RefreshToken.for_user(user)
            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_200_OK
            )
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            from django.utils.http import urlsafe_base64_encode
            from django.utils.encoding import force_bytes

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f"https://your-frontend.com/reset-password?uid={uid}&token={token}"

            send_mail(
                subject='Password Reset on Loopback',
                message=f'Click here to reset your password: {reset_url}',
                from_email='no-reply@loopback.com',
                recipient_list=[email],
            )

        return Response({"message": "A reset link will be sent to your email if it exists."}, status=200)



class PasswordResetConfirmView(APIView):
    def post(self, request):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid user'}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired token'}, status=400)

        user.password = make_password(new_password)
        user.save()
        return Response({'message': 'Password reset successful'})



# Users Profile Creation
# class CreateUserProfileView(CreateAPIView):
#     serializer_class = ProfileSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         profile = serializer.save(user=self.request.user)

#         if profile.role == 'mentee':
#             matched_mentor = search_mentor_for_mentee(profile)
#             if matched_mentor:
#                 Mentorship.objects.create(
#                     mentor=matched_mentor,
#                     mentee=profile,
#                     is_active=True,
#                 )
    

# Users Profile Retrieval and Update



class ProfileUserUpdateView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    
    def perform_update(self, serializer):
        profile = serializer.save()

        # Only run matching logic if profile is being updated to mentee (you can refine this)
        if profile.role == 'mentee' and not Mentorship.objects.filter(mentee=profile).exists():
            matched_mentor = search_mentor_for_mentee(profile)
            if matched_mentor:
                # MatchRequest.objects.get_or_create OR Mentorship.objects.create
                MatchRequest.objects.get_or_create(
                    mentor=matched_mentor,
                    mentee=profile,
                    is_active=True,
                )
        return Response({'message': 'MatchRequest created: mentee {profile.user.username} → mentor {matched_mentor.user.username}'}, status=201)
        # return Response(f"MatchRequest created: mentee {profile.user.username} → mentor {matched_mentor.user.username}")
    




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


class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(loop_mentor=self.request.user) | Goal.objects.filter(loop_mentee=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class WeeklycheckinViewSet(viewsets.ModelViewSet):
    queryset = Weeklycheckin.objects.all()
    serializer_class = WeeklycheckinSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)



class LoopFeedbackViewSet(viewsets.ModelViewSet):
    queryset = LoopFeedback.objects.all()
    serializer_class = LoopFeedbackSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)








# Backend Profile Creation and Operations
class ProfileUserCreate(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    lookup_field = "id"

class ProfileUserUpdate(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    lookup_field = "id"




# Backend Dynamic Use for Matching Only.
class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    

