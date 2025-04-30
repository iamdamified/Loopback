"""
URL configuration for Loopback project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('api.urls')),

    path('auth/registration/', include('dj_rest_auth.registration.urls')),# Google registration
    path('accounts/', include('allauth.urls')),# Gmail login (Google OAuth2 via allauth)

    path('auth/', include('dj_rest_auth.urls')), # Google auth



    # path('auth/social/', include('allauth.socialaccount.urls')),  # Google Login
    # path('users/', include('users.urls'))
    # path('/auth/password/reset/', TemplateView.as_view(template_name="account/password_reset.html"), name='password_reset'),
    # path('auth/password/reset/confirm/<uidb64>/<token>/', TemplateView.as_view(template_name="account/password_reset_done.html"), name='password_reset_confirm'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)