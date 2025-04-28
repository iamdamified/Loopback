from django.urls import path, include
# from rest_framework.authtoken.views import obtain_auth_token
from .views import CustomTokenView, RegisterView, VerifyEmailView, ProfileUserView, InterestViewSet, SkillViewSet, LoginView, MentorshipViewSet, GoalViewSet, WeeklycheckinViewSet,  LoopFeedbackViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import GoogleLogin

router = DefaultRouter()
router.register(r'loops', MentorshipViewSet, basename='loops')
router.register(r'goals', GoalViewSet, basename='goals')
router.register('checkins/', WeeklycheckinViewSet, basename='checkins')
router.register('loop-feedbacks/', LoopFeedbackViewSet, basename='loop-feedbacks')

# FOR BACKEND DYNAMIC MATCHING INPUT DATA
router.register(r'interests', InterestViewSet)
router.register(r'skills', SkillViewSet)

urlpatterns = router.urls

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/<int:uid>/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('token/', CustomTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileUserView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),

    # Google login
    path('google/', GoogleLogin.as_view(), name='google_login'),
    # FOR BACKEND
    path('', include(router.urls)),
    

    
]

