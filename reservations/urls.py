from django.urls import path

from .views import(
    reservations,
    reservation_create,
    reservation_detail,
    reservation_update,
    reservation_delete
)

urlpatterns = [
    path('', reservations, name='reservations'),
    path('create', reservation_create, name='reservation_create'),
    path('<uuid:reservation_uuid>', reservation_detail, name='reservation_detail'),
    path('<uuid:reservation_uuid>/update', reservation_update, name='reservation_update'),
    path('<uuid:reservation_uuid>/delete', reservation_delete, name='reservation_delete'),
]