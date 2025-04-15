from django.urls import path
from .views import ProfileUserView, UserListView, UserDetailView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('profile/', ProfileUserView.as_view(), name='profile')
]