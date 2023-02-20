from django.urls import path
from client import views

urlpatterns = [
    # ...
    path('/profiles', views.profiles, name='profile'),
    path('/create_profile', views.create_profile, name='create_profile'),
    path('/edit_profile', views.edit, name='edit_profile'),
    # ...
]
