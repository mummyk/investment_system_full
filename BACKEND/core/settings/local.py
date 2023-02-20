from .base import *


# Email configuration for authentication
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Pinax referral system
PINAX_REFERRALS_SECURE_URLS = False