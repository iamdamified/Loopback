from django.shortcuts import render, redirect
from .models import User
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
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
from django.http import HttpResponseRedirect
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_framework import permissions
from profiles.models import MentorProfile, MenteeProfile
from rest_framework.permissions import IsAuthenticated


# Create your views here.

User = get_user_model()



# fix for expired sendgrid
class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  # Require email verification
            user.save()

            # Generate token and verification URL
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verify_url = f"http://loopback-f6mg.onrender.com/api/auth/verify-email/{uid}/{token}/"

            # Try to send email
            try:
                send_mail(
                    subject="Verify your Email",
                    message=f"Click the link to verify your account: {verify_url}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False
                )
                return Response(
                    {"message": "Registration successful! Check your email to verify your account."},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                # Log the failure and return the link in the response
                print(f"Failed to send verification email: {e}")
                return Response({
                    "message": "Registration successful, but failed to send verification email.",
                    "verify_url": verify_url,
                }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# RESEND VERIFICATION EMAIL

# class ResendVerificationEmailView(APIView):
#     def post(self, request):
#         email = request.data.get("email")
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

#         if user.verified:
#             return Response({'message': 'Email already verified.'}, status=status.HTTP_400_BAD_REQUEST)

#         # Generate a fresh token and UID
#         token = default_token_generator.make_token(user)
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         verify_url = f"http://loopback-f6mg.onrender.com/api/auth/verify-email/{uid}/{token}/"

        
#         try:
#             # Send the email
#             send_mail(
#                 subject="Resend: Verify your Email",
#                 message=f"Click the link to verify your account: {verify_url}",
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=[user.email],
#                 fail_silently=False
#             )
            
            
#         except Exception as e:
#             print(f"Failed to send verification email: {e}")

#         return Response({'message': 'Verification email resent!'}, status=status.HTTP_200_OK)
    

# fix for expired sendgrid
class ResendVerificationEmailView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user.verified:
            return Response({'message': 'Email already verified.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate token and UID
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verify_url = f"http://loopback-f6mg.onrender.com/api/auth/verify-email/{uid}/{token}/"

        try:
            send_mail(
                subject="Resend: Verify your Email",
                message=f"Click the link to verify your account: {verify_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )
            return Response({'message': 'Verification email resent!'}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Email sending failed: {e}")
            return Response({
                'message': 'Verification email resend failed, but here is your link.',
                'verify_url': verify_url,
                'error': str(e)
            }, status=status.HTTP_200_OK)

    




# Verification/Confirmation of Email

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
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": user.role,
        }, status=status.HTTP_200_OK)



# class CustomTokenRefreshView(TokenRefreshView):
#     serializer_class = CustomTokenRefreshSerializer

# # Google Social Register/login view
# This view returns no google key, just HTML(200 success), redirects automatically and Preview shows User role page
# class CustomGoogleLoginView(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter

#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)

#         user = self.request.user

#         # If user has no role, redirect to frontend with user ID for role selection
#         if user.is_authenticated and not getattr(user, 'role', None):
#             redirect_url = f"https://loop-back-two.vercel.app/user-role?user_id={user.id}"
#             return HttpResponseRedirect(redirect_url)

#         # Ensure token is returned in response
#         token = response.data.get("key") or response.data.get("access")

#         return Response({
#             "key": token,
#             "user_id": user.id,
#             "email": user.email,
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#         })




class CustomGoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def get_response(self):
        # Override to use JWT instead of `key`
        user = self.user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Check role
        if not getattr(user, 'role', None):
            return Response({
                "access": access_token,
                "refresh": str(refresh),
                "message": "Role not set. Redirect to role selector.",
                "redirect_url": f"https://loop-back-two.vercel.app/user-role?user_id={user.id}",
                "user_id": user.id,
                "email": user.email,
                "has_role": False,
            }, status=status.HTTP_200_OK)

        # Return full info if role exists
        return Response({
            "access": access_token,
            "refresh": str(refresh),
            "user_id": user.id,
            "email": user.email,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }, status=status.HTTP_200_OK)



class CompleteGoogleUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role:
            return Response({"detail": "Role already assigned."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserRegistrationSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Mark user as verified/active
        user.is_active = True
        user.save()

        # Create profile
        if user.role == 'mentor':
            profile, _ = MentorProfile.objects.get_or_create(user=user)
        else:
            profile, _ = MenteeProfile.objects.get_or_create(user=user)

        # Update profile fields
        profile_fields = serializer.validated_data
        for field in profile_fields:
            if hasattr(profile, field):
                setattr(profile, field, profile_fields[field])
        profile.save()

        return Response({
            "message": f"{user.role.capitalize()} profile completed successfully.",
            "role": user.role,
            "user_id": user.id,
            "email": user.email,
        }, status=status.HTTP_200_OK)



# Password Reset Request View
# class PasswordResetRequestView(APIView):
#     def post(self, request):
#         email = request.data.get('email')

#         #Require email
#         if not email:
#             return Response(
#                 {"error": "Email field is required."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         user = User.objects.filter(email=email).first()
#         if user:
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             token = default_token_generator.make_token(user)
#             # reset_url = f"http://localhost:3000/reset-password?uid={uid}&token={token}"
#             reset_url = f"https://loop-back-two.vercel.app/reset-password?uid={uid}&token={token}"

#             try:
#                 send_mail(
#                     subject='Password Reset on Loopback',
#                     message=f'Click here to reset your password: {reset_url}',
#                     from_email='Loopback <adekoyadamilareofficial@gmail.com>',
#                     recipient_list=[email],
#                     fail_silently=False
#                 )
#             except Exception as e:
#                 print (e)
#                 return Response(
#                     {"error": "Failed to send reset email. Please try again later."},
#                     status=status.HTTP_500_INTERNAL_SERVER_ERROR
#                 )

#         return Response(
#             {"message": "A reset link will be sent to your email if it exists."},
#             status=status.HTTP_200_OK
#         )

# fix to failed sendgrid
class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response(
                {"error": "Email field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email=email).first()

        if not user:
            return Response(
                {"message": "If that email exists, a reset link will be sent."},
                status=status.HTTP_200_OK
            )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = f"https://loop-back-two.vercel.app/reset-password?uid={uid}&token={token}"

        try:
            send_mail(
                subject='Password Reset on Loopback',
                message=f'Click here to reset your password: {reset_url}',
                from_email='adekoyadamilareofficial@gmail.com',  # Must be SendGrid verified
                recipient_list=[email],
                fail_silently=False
            )
            return Response(
                {'message': 'Password reset link sent successfully!'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(f"Failed to send reset email: {e}")
            return Response(
                {
                    'message': 'Reset link generated, but email sending failed.',
                    'reset_url': reset_url,
                    'error': str(e)
                },
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




class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError as e:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
