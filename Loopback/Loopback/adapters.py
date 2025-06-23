from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Only run if the user is not already connected
        if sociallogin.is_existing:
            return

        email = sociallogin.account.extra_data.get("email")
        if not email:
            return

        try:
            # Try to find an existing user with the same email
            user = User.objects.get(email=email)
            if not SocialAccount.objects.filter(user=user, provider=sociallogin.account.provider).exists():
                sociallogin.connect(request, user)
        except User.DoesNotExist:
            pass