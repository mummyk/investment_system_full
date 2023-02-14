from django.urls import path
from allauth.account.views import logout

urlpatterns = [
    # ...
    path('logout/', logout, name='account_logout'),
    # ...
]
