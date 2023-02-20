from django.urls import path
from home import views


urlpatterns = [
    path('', views.home, name='home'),
    path('contact_us', views.contactUs, name='contact_us'),
    path('about_us', views.aboutUs, name='about_us'),
    path('faqs', views.faqs, name='faqs'),
    path('blog', views.blog, name='blog')
]
