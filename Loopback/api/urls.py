from django.urls import path, include
# from rest_framework.authtoken.views import obtain_auth_token
from users.views import CustomTokenView, RegisterView, ResendVerificationEmailView, VerifyEmailView, PasswordResetRequestView, PasswordResetConfirmView, CustomGoogleLoginView
from matchrequest.views import MatchRequestView, MatchResponseView
from mentorship.views import MentorshipLoopViewSet, DashboardView
from weeklycheckin.views import WeeklyCheckInCreateView
from feedback.views import SubmitFeedbackView
from profiles.views import MentorProfileDetailView, MenteeProfileDetailView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'loops', MentorshipLoopViewSet, basename='mentorshiploop')
# GET /loops/
# POST /loops/
# GET  /loops/<id>/
# PUT/PATCH  /loops/<id>/
# POST/DEACTIVATE  /loops/<id>/deactivate/


# router.register(r'loops', MentorshipViewSet, basename='loops')
# router.register(r'goals', GoalViewSet, basename='goals')
# router.register('checkins/', WeeklycheckinViewSet, basename='checkins')
# router.register('loop-feedbacks/', LoopFeedbackViewSet, basename='loop-feedbacks')
# router.register(r'match-requests', MatchRequestViewSet, basename='match-requests')
    

urlpatterns = router.urls

urlpatterns = [

    # USER ONBOARDING
    path('register/', RegisterView.as_view(), name='register'),
    path('resend-verification/', ResendVerificationEmailView.as_view(), name='resend-verification'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', CustomTokenView.as_view(), name='token_obtain_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgot-password/', PasswordResetRequestView.as_view(), name='forgot-password'),
    path('reset-password-confirm/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    path('auth/google/', CustomGoogleLoginView.as_view(), name='google_login'), # Google register/login

    
    # User Profiles
    path('mentor/profile/', MentorProfileDetailView.as_view(), name='mentor-profile'),
    path('mentee/profile/', MenteeProfileDetailView.as_view(), name='mentee-profile'),



    # Mentee Match Request and Mentor Response
    path("match-request/<int:pk>/request/", MatchRequestView.as_view(), name="match-request"),
    path("match-response/<int:pk>/decision/", MatchResponseView.as_view(), name="match-response"),

    # MENTORSHIP
    path("weekly-checkin/", WeeklyCheckInCreateView.as_view(), name="weekly-checkin"),
    path("loop-feedback/", SubmitFeedbackView.as_view(), name="loop-feedback"),


    # DASHBOARD FROM MENTORSHIP SERIALIZERS AND VIEWS
    path('dashboard/', DashboardView.as_view(), name='mentorship-dashboard'),


    # FOR BACKEND
    path('', include(router.urls)),
    
]

