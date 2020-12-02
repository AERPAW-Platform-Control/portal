from uuid import UUID
import uuid

from django.utils import timezone
from django.shortcuts import get_object_or_404

from experiments.models import Experiment
from resources.models import Resource
from resources.resources import remove_units, update_units
from .models import Reservation,ReservationStatusChoice
from accounts.models import AerpawUser

def create_new_reservation(request, form, experiment_uuid):
    """

    :param request:
    :param form:
    :return:
    """
    reservation = Reservation()
    reservation.uuid = uuid.uuid4()
    reservation.name = form.cleaned_data.get('name')
    try:
        reservation.description = form.cleaned_data.get('description')
    except ValueError as e:
        print(e)
        reservation.description = None

    reservation.experiment=get_object_or_404(Experiment, uuid=UUID(str(experiment_uuid)))  

    reservation.resource = form.cleaned_data.get('resource')
    reservation.units = form.cleaned_data.get('units')

    reservation.start_date = form.cleaned_data.get('start_date')
    reservation.end_date = form.cleaned_data.get('end_date')

    is_available = remove_units(reservation.resource,int(reservation.units),reservation.start_date,reservation.end_date)
    if not is_available:
        reservation.state=ReservationStatusChoice.FAILURE.value
        print("The resource is not available at this time")
    else:
        reservation.state=ReservationStatusChoice.SUCCESS.value

    reservation.save()
    reservation.experiment.reservation_of_experiment.add(reservation)
    reservation.save()

    return str(reservation.uuid)


def update_existing_reservation(request, original_units, reservation, form):
    """
    Create new AERPAW reservation

    :param request:
    :param form:
    :return:
    """
    reservation.start_date = form.cleaned_data.get('start_date')
    reservation.end_date = form.cleaned_data.get('end_date')
    is_available = update_units(reservation.resource,int(reservation.units),original_units,reservation.start_date,reservation.end_date)
    if not is_available:
        reservation.state=ReservationStatusChoice.FAILURE.value
        print("The resource is not available at this time")
    else:
        reservation.state=ReservationStatusChoice.SUCCESS.value

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
        update_units(reservation.resource,0, int(reservation.units),reservation.start_date,reservation.end_date)
        reservation.delete()
        return True
    except Exception as e:
        print(e)
        raise RuntimeError('Failed in update_units') from e
    return False


def get_reservation_list(request):
    """

    :param request:
    :return:
    """
    if request.user.is_superuser:
        reservations = Reservation.objects.order_by('name')
    else:
        experiment_id=request.session['experiment_id']
        ex=Experiment.objects.get(id=experiment_id)
        reservations = Reservation.objects.filter(experiment=ex).order_by('name')
    return reservations