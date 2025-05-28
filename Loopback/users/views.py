from django.shortcuts import render, redirect
from .models import User
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str
from django.utils.encoding import force_bytes
from django.contrib.auth.hashers import make_password
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.http import HttpResponseRedirect

# Create your views here.

User = get_user_model()

# User Registrations with Verification
class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  # Block login until email is verified
            user.save()

            # Generate email verification token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            verify_url = f"http://loopback-f6mg.onrender.com/api/auth/verify-email/{uid}/{token}/"

            send_mail(
                subject="Verify your Email",
                message=f"Click the link to verify your account: {verify_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email]
            )

            return Response(
                {'message': 'Registration successful! Check your email to verify your account.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# Verification of Email

class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            # Decode base64 uid to get user ID
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.verified = True  
            user.is_active = True
            user.save()
            # return Response({'message': 'Email verified! You can now log in.'}, status=status.HTTP_200_OK)
            return HttpResponseRedirect('http://localhost:3000/verify')

        return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
    



    
class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # Generate tokens and validate credentials
        response = super().post(request, *args, **kwargs)

        # Now, we can access the authenticated user
        token = response.data.get("access")
        if token:
            access_token = AccessToken(token) # Use the token to get the user
            user_id = access_token["user_id"]
            first_name = access_token["first_name"]
            last_name = access_token["last_name"]
            email = access_token["email"]
            role = access_token["role"]

            User = get_user_model()  # Fetch the actual user object
            user = User.objects.get(id=user_id, first_name=first_name, last_name=last_name, email=email, role=role)

            if not user.role: # Check for role
                raise AuthenticationFailed('Please complete your profile by selecting a role.')

        return response


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        # Handle invalid credentials
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Handle inactive users
        if not user.is_active:
            return Response({"error": "Account is inactive"}, status=status.HTTP_403_FORBIDDEN)

        # Handle missing role
        if not hasattr(user, 'role') or not user.role:
            return Response({"error": "Please complete your profile by selecting a role."}, status=status.HTTP_403_FORBIDDEN)

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                # "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "role": user.role,
            },
            status=status.HTTP_200_OK
        )



# Social login view
class CustomGoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # token = response.data.get("access_token")
        user = self.request.user
        # if user.is_authenticated and not user.role:
        if user.is_authenticated and not getattr(user, 'role', None):
            # Redirect to frontend with user ID for role selection
            redirect_url = f"http://localhost:3000/user-role?user_id={user.id}"
            return HttpResponseRedirect(redirect_url)

        return response



class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')

        #Require email
        if not email:
            return Response(
                {"error": "Email field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email=email).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f"http://loopback-f6mg.onrender.com/reset-password/?uid={uid}&token={token}"

            try:
                send_mail(
                    subject='Password Reset on Loopback',
                    message=f'Click here to reset your password: {reset_url}',
                    from_email='adekoyadamilareofficial@gmail.com',  # Must be verified with SendGrid!
                    recipient_list=[email],
                )
            except Exception as e:
                print (e)
                return Response(
                    {"error": "Failed to send reset email. Please try again later."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # Always return a generic message
        return Response(
            {"message": "A reset link will be sent to your email if it exists."},
            status=status.HTTP_200_OK
        )

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


