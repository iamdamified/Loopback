from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token
from .views import CustomTokenView, RegisterView, VerifyEmailView, ProfileUserView, LoginView, MentorshipViewSet, GoalViewSet, WeeklycheckinViewSet,  LoopFeedbackViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import GoogleLogin

router = DefaultRouter()
router.register(r'loops', MentorshipViewSet, basename='')
router.register(r'goals', GoalViewSet)
router.register(r'checkins', WeeklycheckinViewSet)
router.register(r'loop-feedbacks', LoopFeedbackViewSet)

urlpatterns = router.urls

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/<int:uid>/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', CustomTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileUserView.as_view(), name='profile'),

    # Google login
    path('google/', GoogleLogin.as_view(), name='google_login'),

    

    
]