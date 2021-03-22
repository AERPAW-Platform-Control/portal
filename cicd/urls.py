from django.urls import path
from django.conf.urls import include

from .views import(
    cicd,
    cicd_create,
    cicd_detail,
    cicd_update,
    cicd_delete
)

urlpatterns = [
    path('', cicd, name='cicd'),
    path('create', cicd_create, name='cicd_create'),
    path('<uuid:cicd_uuid>', cicd_detail, name='cicd_detail'),
    path('<uuid:cicd_uuid>/update', cicd_update, name='cicd_update'),
    path('<uuid:cicd_uuid>/delete', cicd_delete, name='cicd_delete'),
]
