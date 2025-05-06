from django.shortcuts import render
from users.models import User
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.hashers import make_password

# Create your views here.


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
            reset_url = f"http://localhost:8000/api/auth/reset-password-confirm/?uid={uid}&token={token}"

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