from django.urls import path, include
# from rest_framework.authtoken.views import obtain_auth_token
from users.views import CustomTokenView, RegisterView, VerifyEmailView, LoginView,  PasswordResetRequestView, PasswordResetConfirmView
from matchrequest.views import MatchRequestViewSet
from mentorship.views import MentorshipViewSet
from goal.views import GoalViewSet
from weeklycheckin.views import WeeklycheckinViewSet
from feedback.views import LoopFeedbackViewSet
from profiles.views import ProfileUserUpdateView, InterestViewSet, SkillViewSet
from users.views import GoogleLogin, complete_role
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'loops', MentorshipViewSet, basename='loops')
router.register(r'goals', GoalViewSet, basename='goals')
router.register('checkins/', WeeklycheckinViewSet, basename='checkins')
router.register('loop-feedbacks/', LoopFeedbackViewSet, basename='loop-feedbacks')
router.register(r'match-requests', MatchRequestViewSet, basename='match-requests')

# FOR BACKEND DYNAMIC MATCHING INPUT DATA
router.register(r'interests', InterestViewSet)
router.register(r'skills', SkillViewSet)

urlpatterns = router.urls

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/<int:uid>/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('token/', CustomTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),# to be added
    path('profile/', ProfileUserUpdateView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', PasswordResetRequestView.as_view(), name='forgot-password'), # to be added
    path('reset-password-confirm/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'), # to be added
    

    # Google login
    path('google/', GoogleLogin.as_view(), name='google_login'),# to be added
    path('complete-role/', complete_role, name='complete_role'),# to be added

    # FOR BACKEND
    path('', include(router.urls)),
    

    
]

