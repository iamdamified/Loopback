from django.urls import path
from .views import ProfileUserView
from rest_framework.authtoken.views import obtain_auth_token
from .views import CustomTokenView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('profile/', ProfileUserView.as_view(), name='profile'),
    path('token/', CustomTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]