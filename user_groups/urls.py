# accounts/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('user_groups', views.user_groups, name='user_groups'),
    # path('user_projects', views.users, name='users'),
    # path('user_experiments', views.users, name='users'),
]
