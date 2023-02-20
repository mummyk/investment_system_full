from django.urls import path
from investments import views

urlpatterns = [
    path('invest', views.invest, name='invest'),
]
