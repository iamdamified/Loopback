from django.shortcuts import render, redirect
from users.models import User

from django.contrib.auth.decorators import login_required

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView




@login_required
def complete_role(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        if role:
            request.user.role = role
            request.user.save()
            return redirect('home')  # Or dashboard page
    return render(request, 'complete_roles.html')


# Social login view
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        user = request.user
        if user.is_authenticated and not user.role:
            return redirect('complete_role')

        return response




