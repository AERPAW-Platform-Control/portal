from uuid import UUID
import uuid

from django.utils import timezone
from django.shortcuts import get_object_or_404

from experiments.models import Experiment
from resources.models import Resource
from .models import Reservation
from accounts.models import AerpawUser

def create_new_reservation(request, form, experiment_uuid):
    """

    :param request:
    :param form:
    :return:
    """
    reservation = Reservation()
    reservation.uuid = uuid.uuid4()
    reservation.name = form.data.getlist('name')[0]
    try:
        reservation.description = form.data.getlist('description')[0]
    except ValueError as e:
        print(e)
        reservation.description = None

    reservation.experiment=get_object_or_404(Experiment, uuid=UUID(str(experiment_uuid)))  

    resource_id = form.data.getlist('resource')[0]
    reservation.resource = Resource.objects.get(id=int(resource_id))

    reservation.units = form.data.getlist('units')[0]
    reservation.created_by = request.user
    reservation.created_date = timezone.now()
    reservation.modified_by = reservation.created_by
    reservation.modified_date = reservation.created_date
    reservation.save()

    return str(reservation.uuid)


def update_existing_reservation(request, reservation, form):
    """
    Create new AERPAW reservation

    :param request:
    :param form:
    :return:
    """
    reservation.modified_by = request.user
    reservation.modified_date = timezone.now()

    reservation.save()
    return str(reservation.uuid)


def delete_existing_reservation(request, reservation):
    """

    :param request:
    :param reservation:
    :return:
    """
    try:
        reservation.delete()
        return True
    except Exception as e:
        print(e)
    return False


def get_reservation_list(request):
    """

    :param request:
    :return:
    """
    if request.user.is_superuser:
        reservations = Reservation.objects.order_by('name')
    else:
        reservations = Reservation.objects.order_by('name')
    return reservations