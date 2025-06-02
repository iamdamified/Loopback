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
from allauth.socialaccount.models import SocialAccount
from django.http import HttpResponseRedirect

# Create your views here.

User = get_user_model()

# User Registrations with Verification(Mentors and Mentees)
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


class ResendVerificationEmailView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user.verified:
            return Response({'message': 'Email already verified.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a fresh token and UID
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verify_url = f"http://loopback-f6mg.onrender.com/api/auth/verify-email/{uid}/{token}/"

        # Send the email
        send_mail(
            subject="Resend: Verify your Email",
            message=f"Click the link to verify your account: {verify_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )

        return Response({'message': 'Verification email resent!'}, status=status.HTTP_200_OK)


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
            return HttpResponseRedirect('https://loop-back-two.vercel.app/verify')

        return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
    



# Login View with JWT Token Generation
class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed as e:
            raise e

        user = serializer.user
        # Handle inactive users
        if not user.is_active:
            return Response({"error": "Account is inactive"}, status=status.HTTP_403_FORBIDDEN)

        if not user.role:
            raise AuthenticationFailed('Please complete your profile by selecting a role.')

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            "refresh": str(refresh),
            "access": str(access),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": user.role,
        }, status=status.HTTP_200_OK)



# # Google Social Register/login view
# class CustomGoogleLoginView(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter

#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)

#         # token = response.data.get("access_token")
#         user = self.request.user
#         # if user.is_authenticated and not user.role:
#         if user.is_authenticated and not getattr(user, 'role', None):
#             # Redirect to frontend with user ID for role selection
#             redirect_url = f"https://loop-back-two.vercel.app/user-role?user_id={user.id}"
#             return HttpResponseRedirect(redirect_url)

#         return response




# class CustomGoogleLoginView(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter

#     def post(self, request, *args, **kwargs):
#         # Extract the token from the request
#         access_token = request.data.get("access_token")

#         if not access_token:
#             return Response({"error": "Access token is required"}, status=status.HTTP_400_BAD_REQUEST)
#         response = super().post(request, *args, **kwargs)
#         # At this point, self.request.user is the logged-in user from Google
#         google_user = self.request.user
#         # Get Google email from the social login response
#         email = google_user.email if google_user and google_user.email else None

#         if email:
#             try:
#                 existing_user = User.objects.get(email=email)

#                 if existing_user.verified and existing_user.role:
#                     if not SocialAccount.objects.filter(user=existing_user).exists():
#                         social_account = SocialAccount.objects.filter(user=google_user).first()
#                         if social_account:
#                             social_account.user = existing_user
#                             social_account.save()
#                     # Force login of the existing user
#                     self.request.user = existing_user
#                     # If verified and role exists, my frontend will handle login redirect
#                     return Response({
#                         "detail": "Login successful.",
#                         "user_id": existing_user.id,
#                         "email": existing_user.email
#                     }, status=status.HTTP_200_OK)

#                 elif existing_user.verified and not existing_user.role:
#                     # Redirect to role selection if no role
#                     return HttpResponseRedirect(
#                         f"https://loop-back-two.vercel.app/user-role?user_id={existing_user.id}"
#                     )

#             except User.DoesNotExist:
#                 #Google OAuth2 flow continue (new user will be created)
#                 pass

#         return response


class CustomGoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def post(self, request, *args, **kwargs):
        access_token = request.data.get("access_token")
        if not access_token:
            return Response({"error": "Access token is required"}, status=status.HTTP_400_BAD_REQUEST)
        # Temporarily complete the login without saving
        try:
            # Stimulate the social login process
            login = self.adapter_class().complete_login(self.request, None)
            login.token = access_token
            login.state = SocialLoginView.serializer_class().validate(request.data)
            email = login.account.extra_data.get("email")
        except Exception:
            return Response({"error": "Invalid Google login attempt."}, status=status.HTTP_400_BAD_REQUEST)

        if email:
            try:
                existing_user = User.objects.get(email=email)

                if existing_user.verified and existing_user.role:
                    # Check if social account already exists
                    if not SocialAccount.objects.filter(user=existing_user).exists():
                        # Create a new SocialAccount and link it
                        login.user = existing_user
                        login.save(request, connect=True)
                    self.request.user = existing_user

                    return Response({
                        "detail": "Login successful.",
                        "user_id": existing_user.id,
                        "email": existing_user.email
                    }, status=status.HTTP_200_OK)

                elif existing_user.verified and not existing_user.role:
                    return HttpResponseRedirect(
                        f"https://loop-back-two.vercel.app/user-role?user_id={existing_user.id}"
                    )

            except User.DoesNotExist:
                # Proceed with the default flow for new users
                pass

        # Fall back to default Google login flow
        response = super().post(request, *args, **kwargs)
        return response

# Password Reset Request View
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
            # reset_url = f"http://localhost:3000/reset-password?uid={uid}&token={token}"
            reset_url = f"https://loop-back-two.vercel.app/reset-password?uid={uid}&token={token}"

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

        return Response(
            {"message": "A reset link will be sent to your email if it exists."},
            status=status.HTTP_200_OK
        )

# Password Reset Success View
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
        # redirect_url = f"http://localhost:3000/password-success-page?user_id={user.id}" hoping frontend will handle this and ask 
        # return HttpResponseRedirect(redirect_url)





























# class LoginView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user = authenticate(email=email, password=password)

#         # Handle invalid credentials
#         if not user:
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#         # Handle inactive users
#         if not user.is_active:
#             return Response({"error": "Account is inactive"}, status=status.HTTP_403_FORBIDDEN)

#         # Handle missing role
#         if not hasattr(user, 'role') or not user.role:
#             return Response({"error": "Please complete your profile by selecting a role."}, status=status.HTTP_403_FORBIDDEN)

#         # Generate tokens
#         refresh = RefreshToken.for_user(user)
#         return Response(
#             {
#                 "refresh": str(refresh),
#                 "access": str(refresh.access_token),
#                 # "username": user.username,
#                 "first_name": user.first_name,
#                 "last_name": user.last_name,
#                 "email": user.email,
#                 "role": user.role,
#             },
#             status=status.HTTP_200_OK
#         )



# class CustomTokenView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer

#     def post(self, request, *args, **kwargs):
#         # Generate tokens and validate credentials
#         response = super().post(request, *args, **kwargs)

#         # Now, we can access the authenticated user
#         token = response.data.get("access")
#         if token:
#             access_token = AccessToken(token) # token to get the user
#             user_id = access_token["user_id"]

#             User = get_user_model()  # Fetch the actual user object
#             user = User.objects.get(id=user_id)

#             if not user.role: # Check for role
#                 raise AuthenticationFailed('Please complete your profile by selecting a role.')

#         # return response
#         return Response(
#             {
                
#                 "access": access_token,
#                 "refresh": str(RefreshToken.for_user(user)),
#                 # "username": user.username,
#                 "first_name": user.first_name,
#                 "last_name": user.last_name,
#                 "email": user.email,
#                 "role": user.role,
#             },
#             status=status.HTTP_200_OK
#         )