import uuid

from django.utils import timezone

from .models import Experiment
from reservations.models import Reservation
from accounts.models import AerpawUser
from projects.models import Project


def create_new_experiment(request, form):
    """

    :param request:
    :param form:
    :return:
    """
    experiment = Experiment()
    experiment.uuid = uuid.uuid4()
    experiment.name = form.data.getlist('name')[0]
    try:
        experiment.description = form.data.getlist('description')[0]
    except ValueError as e:
        print(e)
        experiment.description = None

    experiment.created_by = request.user
    experiment.created_date = timezone.now()
    experiment.save()

    experimenter_id_list = form.data.getlist('experimenter')
    update_experimenter(experiment, experimenter_id_list)
    experiment.save()

    experiment_reservation_id_list = form.data.getlist('experiment_reservations')
    update_experiment_reservations(experiment, experiment_reservation_id_list)
    experiment.save()
    return str(experiment.uuid)


def update_experimenter(experiment, experimenter_id_list):
    """

    :param experiment:
    :param experiment_reservation_id_list:
    :return:
    """
    # clear current experimenter
    experiment.experimenter.clear()
    # add members from experimenter_id_update_list
    for experimenter_id in experimenter_id_update_list:
        experiment_experimenter = AerpawUser.objects.get(id=int(experimenter_id))
        experiment.experimenter.add(experiment_experimenter)


def update_existing_experiment(request, experiment, form):
    """
    Create new AERPAW Experiment

    :param request:
    :param form:
    :return:
    """
    experiment.modified_by = request.user
    experiment.modified_date = timezone.now()
    experiment.save()
    experiment_member_id_list = form.data.getlist('experiment_reservations')
    update_experiment_reservations(experiment, experiment_reservation_id_list)
    experiment.save()
    return str(experiment.uuid)


def delete_existing_experiment(request, experiment):
    """

    :param request:
    :param experiment:
    :return:
    """
    try:
        experiment.delete()
        return True
    except Exception as e:
        print(e)
    return False


def get_experiment_list(request):
    """

    :param request:
    :return:
    """
    if request.user.is_superuser:
        experiments = Experiment.objects.order_by('name')
    else:
        experiments = Experiment.objects.order_by('name')
    return experiments