from django.urls import path
from django.conf.urls import include

from reservations import views

from .views import(
    experiments,
    experiment_create,
    experiment_detail,
    experiment_update,
    experiment_delete,
    experiment_initiate,
    experiment_manifest
)

urlpatterns = [
    path('', experiments, name='experiments'),
    path('create', experiment_create, name='experiment_create'),
    path('<uuid:experiment_uuid>', experiment_detail, name='experiment_detail'),
    path('<uuid:experiment_uuid>/update', experiment_update, name='experiment_update'),
    path('<uuid:experiment_uuid>/delete', experiment_delete, name='experiment_delete'),
    path('<uuid:experiment_uuid>/initiate', experiment_initiate, name='experiment_initiate'),
    path('<uuid:experiment_uuid>/manifest', experiment_manifest, name='experiment_manifest'),
    path('', include(('reservations.urls', 'reservations'), namespace='reservations')),
]