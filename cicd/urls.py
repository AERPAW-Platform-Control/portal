from django.urls import path
from django.conf.urls import include

from .views import(
    cicd,
    cicd_host_info,
    cicd_create,
    cicd_host_info_create,
    cicd_detail,
    cicd_host_info_detail,
    cicd_update,
    cicd_delete
)

urlpatterns = [
    path('', cicd, name='cicd'),
    path('hostinfo', cicd_host_info, name='cicd_host_info'),
    path('create', cicd_create, name='cicd_create'),
    path('hostinfo/create', cicd_host_info_create, name='cicd_host_info_create'),
    path('<uuid:cicd_uuid>', cicd_detail, name='cicd_detail'),
    path('hostinfo/<uuid:cicd_host_info_uuid>', cicd_host_info_detail, name='cicd_host_info_detail'),
    path('<uuid:cicd_uuid>/update', cicd_update, name='cicd_update'),
    path('<uuid:cicd_uuid>/delete', cicd_delete, name='cicd_delete'),
]
