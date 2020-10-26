from django.urls import path

from .views import(
    experiments,
    experiment_create,
    experiment_detail,
    experiment_update,
    experiment_delete
)

urlpatterns = [
    path('', experiments, name='experiments'),
    path('create', experiment_create, name='experiment_create'),
    path('<uuid:experiment_uuid>', experiment_detail, name='experiment_detail'),
    path('<uuid:experiment_uuid>/update', experiment_update, name='experiment_update'),
    path('<uuid:experiment_uuid>/delete', experiment_delete, name='experiment_delete'),
]