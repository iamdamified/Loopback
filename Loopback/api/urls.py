from django.urls import path, include
# from rest_framework.authtoken.views import obtain_auth_token
from users.views import CustomTokenView, RegisterView, ResendVerificationEmailView, VerifyEmailView, PasswordResetRequestView, PasswordResetConfirmView, CustomGoogleLoginView
from matchrequest.views import MatchRequestView, MatchResponseView, MentorMatchesRequestsView, MenteeMatchesRequestsView, CreateMeetingScheduleView, MentorMeetingScheduleView, MenteeMeetingScheduleView
from mentorship.views import CreateMentorshipLoopView, MentorLoopsListView, MenteeLoopsListView
from weeklycheckin.views import WeeklyCheckInListCreateView, WeeklyCheckInUpdateView
from feedback.views import SubmitFeedbackView, UserFeedbackListView, AllFeedbackListView
from profiles.views import MentorProfileDetailView, MenteeProfileDetailView, AllMentorsListView, SuggestedMentorsListView, AllMenteesListView, MenteeDetailView, MentorDetailView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register(r'loops', MentorshipLoopViewSet, basename='mentorshiploop')
# GET /loops/
# POST /loops/
# GET  /loops/<id>/
# PUT/PATCH  /loops/<id>/
# POST/DEACTIVATE  /loops/<id>/deactivate/

    

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

    
    # User Profile Management and Listing, and Detail Views
    path('mentor/profile/', MentorProfileDetailView.as_view(), name='mentor-profile'),
    path('mentee/profile/', MenteeProfileDetailView.as_view(), name='mentee-profile'),
    path('all/mentors/', AllMentorsListView.as_view(), name='all-mentors'),
    path('mentor/detail/<int:id>/', MentorDetailView.as_view(), name='mentor-detail'),
    path('all/mentees/', AllMenteesListView.as_view(), name='all-mentees'),
    path('mentee/detail/<int:id>/', MenteeDetailView.as_view(), name='mentor-detail'),
    


    # MATCHING SYSTEM
    # Mentee Match Request and Mentor Response, and Records
    path("suggested-mentors/", SuggestedMentorsListView.as_view(), name="suggested-mentors"),
    path("match-request/", MatchRequestView.as_view(), name="match-request"),
    path("match-response/<match_request_id>/", MatchResponseView.as_view(), name="match-response"),
    path('match-requests/mentors/', MentorMatchesRequestsView.as_view(), name='mentor-match-requests'),
    path('match-requests/mentees/', MenteeMatchesRequestsView.as_view(), name='mentee-match-requests'),
    path('meeting-schedule/<int:match_request_id>/', CreateMeetingScheduleView.as_view(), name='create-meeting'),


    #Introductory Meeting Schedule
    path('meeting/mentor/', MentorMeetingScheduleView.as_view(), name='mentor-meetings'),
    path('meeting/mentee/', MenteeMeetingScheduleView.as_view(), name='mentee-meetings'),

    # MENTORSHIP
    path('loops/create/', CreateMentorshipLoopView.as_view(), name='create_mentorship_loop'),
    path('loops/mentor/', MentorLoopsListView.as_view(), name='mentor-loops'),
    path('loops/mentee/', MenteeLoopsListView.as_view(), name='mentee-loops'),
    # /?status=ongoing
    # /?status=completed
    # /?status=pending
    

    # Weekly Checkins
    path("weekly-checkin/", WeeklyCheckInListCreateView.as_view(), name="weekly-checkin"),
    path("weekly-checkin/<int:pk>/", WeeklyCheckInUpdateView.as_view(), name="weekly-checkin-update"),

    # Mentorship Feedbacks
    path("mentorship-feedback/", SubmitFeedbackView.as_view(), name="mentorship-feedback"),
    path('user-feedback/', UserFeedbackListView.as_view(), name='user-feedback-list'),
    path('all-feedback/', AllFeedbackListView.as_view(), name='all-feedback-list'),


    # DASHBOARD FROM MENTORSHIP SERIALIZERS AND VIEWS
    # path('dashboard/', DashboardView.as_view(), name='mentorship-dashboard'),


    # FOR BACKEND
    path('', include(router.urls)),
    
]

