from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import CustomTokenView, RegisterView, VerifyEmailView, ProfileUserView, LoginView, MentorshipViewSet, GoalViewSet, WeeklycheckinViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'loops', MentorshipViewSet)
router.register(r'goals', GoalViewSet)
router.register(r'checkins', WeeklycheckinViewSet)

urlpatterns = router.urls

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/<int:uid>/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', CustomTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileUserView.as_view(), name='profile'),
]