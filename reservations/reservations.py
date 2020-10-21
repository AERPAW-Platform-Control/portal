import uuid

from django.utils import timezone

from experiments.models import Experiment
from resources.models import Resource
from .models import Reservation
from accounts.models import AerpawUser

def create_new_reservation(request, form):
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

    reservation.experimenter = Project.objects.get(
        id=int(form.data.getlist('project_members')[0])
    )

    reservation.created_by = request.user
    reservation.created_date = timezone.now()
    reservation.modified_by = reservation.created_by
    reservation.modified_date = reservation.created_date
    reservation.save()
    reservation_reservation_id_list = form.data.getlist('reservation_reservations')
    update_reservation_reservations(reservation, reservation_reservation_id_list)
    reservation.save()
    return str(reservation.uuid)


def update_reservation_reservations(reservation, reservation_reservation_id_list):
    """

    :param reservation:
    :param reservation_reservation_id_list:
    :return:
    """
    # clear current reservation reservation
    reservation.reservation_reservations.clear()
    # add members from reservation_member_id_update_list
    for reservation_id in reservation_reservation_id_list:
        reservation_reservation = AerpawUser.objects.get(id=int(reservation_id))
        reservation.reservation_reservations.add(reservation_reservation)
    reservation.save()
    # add principal_investigator to reservation_members if not already there
    if reservation.reservation not in reservation.reservation_reservations.all():
        reservation.reservation_reservations.add(reservation.reservation)
        reservation.save()


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
    reservation_member_id_list = form.data.getlist('reservation_reservations')
    update_reservation_reservations(reservation, reservation_reservation_id_list)
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