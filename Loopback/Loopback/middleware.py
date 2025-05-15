from django.shortcuts import redirect
from django.urls import reverse

EXEMPT_URLS = [
    '/admin/',
    '/api/auth/complete_role/', # api/auth/complete_role/
    '/api/auth/login/',     # api/auth/login/
    '/auth/google/',  # api/auth/google/ Google login endpoint
    '/api/auth/token/',   # Token login endpoint
    '/api/auth/token/refresh/', # Token refresh endpoint
    '/api/auth/register/', # Register endpoint
    '/api/auth/verify-email/<int:uid>/<str:token>/', # Verify email endpoint
    '/api/auth/forgot-password/', # Password reset request endpoint
    '/api/auth/reset-password-confirm/', # Password reset confirm endpoint
    '/api/auth/profile/' # Profile update endpoint
]

class RoleRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        if request.user.is_authenticated:
            if not request.user.role and not any(path.startswith(url) for url in EXEMPT_URLS):
                return redirect(reverse('complete_role'))  # view  in urls.py front frontend
        
        response = self.get_response(request)
        return response