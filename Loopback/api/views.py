from django.shortcuts import render
from users.models import Profile
from .serializers import UserSerializer, ProfileSerializer, CustomTokenObtainPairSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings


class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# Create your views here.

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
        role = request.data.get('role', 'mentee')

        user = User.objects.create_user(username=username, email=email, password=password, role=role)
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

class LoginView(APIView):
    def post(self, request):
        from django.contrib.auth import authenticate
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_200_OK
            )
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



# Profile Creation and Operations
class ProfileUserCreate(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    # lookup_field = "id"

    def get_object(self):
        return self.request.user.profile
    

class ProfileUserView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    lookup_field = "id"

    def get_object(self):
        return self.request.user.profile



















    

