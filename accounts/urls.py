# accounts/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('signup', views.signup, name='signup'),
    path('credential', views.credential, name='credential'),
]
