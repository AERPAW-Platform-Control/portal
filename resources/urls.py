from django.urls import path

from .views import(
    resources,
    resource_create,
    resource_detail,
    resource_update,
    resource_delete
)

urlpatterns = [
    path('', resources, name='resources'),
    path('create', resource_create, name='resource_create'),
    path('<uuid:resource_uuid>', resource_detail, name='resource_detail'),
    path('<uuid:resource_uuid>/update', resource_update, name='resource_update'),
    path('<uuid:resource_uuid>/delete', resource_delete, name='resource_delete'),
]