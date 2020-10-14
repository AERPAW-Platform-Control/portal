from django.urls import path

from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('create', views.project_create, name='project_create'),
    path('<uuid:project_uuid>', views.project_detail, name='project_detail'),
    path('<uuid:project_uuid>/update', views.project_update, name='project_update'),
    path('<uuid:project_uuid>/delete', views.project_delete, name='project_delete'),
]
