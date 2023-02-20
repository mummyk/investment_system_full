"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include, re_path
from dj_rest_auth.registration.views import VerifyEmailView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('accounts/', include('allauth.urls')),
    path('referrals', include('referrals.urls')),
    path('client', include('client.urls')),
    path('payments', include('payments.urls')),
    path('dashboard', include('dashboard.urls')),
    path('investments', include('investments.urls')),
    path('', include('home.urls')),

    # Email verification
    path('dj-rest-auth/account-confirm-email/', VerifyEmailView.as_view(),
         name='account_email_verification_sent'),
]

# /dj-rest-auth/registration/resend-email/ ----- to resend the verification email
