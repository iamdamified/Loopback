from allauth.account.adapter import DefaultAccountAdapter

class NoRedirectAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        return "/"
    
    def get_signup_redirect_url(self, request):
        return "/"