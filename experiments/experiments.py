import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from .models import Experiment, StageChoice
from reservations.models import Reservation
from accounts.models import AerpawUser
from projects.models import Project
from profiles.models import Profile
from profiles.profiles import *
from resources.resources import *
from resources.models import Resource
import aerpawgw_client
from aerpawgw_client.rest import ApiException
from aerpawgw_client.models.vnode import Vnode
from aerpawgw_client.models.resource import Resource as Manifest
from datetime import datetime
import logging
import os
import sys


logger = logging.getLogger(__name__)


def create_new_experiment(request, form, project_id):
    """

    :param request:
    :param form:
    :return:
    """
    experiment = Experiment()
    experiment.uuid = uuid.uuid4()
    #request.session['experiment_uuid'] = experiment.uuid
    experiment.name = form.data.getlist('name')[0]
    try:
        experiment.description = form.data.getlist('description')[0]
    except ValueError as e:
        print(e)
        experiment.description = None
    experiment.created_by = request.user
    experiment.created_date = timezone.now()
    experiment.save()

    experiment.project = Project.objects.get(id=str(project_id))
    experiment.experimenter.add(request.user)
    experiment.modified_by = experiment.created_by
    experiment.modified_date = experiment.created_date
    experiment.stage = 'Idle'
    experiment.save()

    # experimenter_id_list = form.data.getlist('experimenter')
    # update_experimenter(experiment, experimenter_id_list)
    # experiment.save()

    # try:
    #     experiment.project = Project.objects.get(id=int(form.data.getlist('project')[0]))
    #     experiment.project.experiment_of_project.add(experiment)
    #     experiment.profile = Profile.objects.get(id=int(form.data.getlist('profile')[0]))
    #     experiment.save()
    # except ValueError as e:
    #     print(e)
    #     experiment.project = None

    #try:
    #    reservation_id_list=form.data.getlist('reservation')
    #    if not reservation_id_list:
    #        reservation_id = reservation_id_list[0]
    #        experiment.reservations = Reservation.objects.get(id=int(reservation_id))
    #except ValueError as e:
    #    print(e)
    #    experiment.reservations= None
    #experiment.save()

    return str(experiment.uuid)


def update_experimenter(experiment, experimenter_id_list):
    """

    :param experiment:
    :param experimenter_id_list:
    :return:
    """
    # clear current experimenter
    experiment.experimenter.clear()
    # add members from experimenter_id_update_list
    for experimenter_id in experimenter_id_list:
        experiment_experimenter = AerpawUser.objects.get(id=int(experimenter_id))
        experiment.experimenter.add(experiment_experimenter)


def update_existing_experiment(request, experiment, form):
    """
    Create new AERPAW Experiment

    :param request:
    :param form:
    :return:
    """
    try:
        experiment.modified_by = request.user
        experiment.modified_date = timezone.now()
        experiment.stage = form.data.getlist('stage')[0]
        experiment.save()
        experiment.profile = Profile.objects.get(id=int(form.data.getlist('profile')[0]))
        experiment.save()
    except ValueError as e:
        print(e)
    #experiment_reservation_id_list = form.data.getlist('experiment_reservations')
    #update_experiment_reservations(experiment, experiment_reservation_id_list)
    return str(experiment.uuid)

def send_exepriment_update_email(experiment):
    subject = 'AERPAW experiment stage update'
    message = 'This experiment requires a stage update:' + str(experiment)
    email_from = settings.EMAIL_HOST_USER
    recipient_list=[]
    recipient_list.append(settings.EMAIL_ADMIN_USER)
    send_mail(subject, message, email_from, recipient_list )

def update_experiment_reservations(experiment, experiment_reservation_id_list):
    """

    :param experiment:
    :param experimenter_id_list:
    :return:
    """
    # clear current reservations
    #experiment.reservations.clear()
    # add reservations from experimenter_id_update_list
    for res_id in experiment_reservation_id_list:
        experiment_reservation = Reservation.objects.get(id=int(res_id))
        experiment.reservations.add(experiment_reservation)


def delete_existing_experiment(request, experiment):
    """

    :param request:
    :param experiment:
    :return:
    """
    try:
        if experiment.profile is not None and is_emulab_profile(experiment.stage):
            # instance on emulab should be terminated first
            emulab_deleted = terminate_emulab_instance(request, experiment)
            if emulab_deleted is False:
                return False
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
        experiments = Experiment.objects.filter(experimenter=request.user).order_by('name')
    return experiments


def initiate_emulab_instance(request, experiment):
    """
    Start experiment instance status on Emulab

    :param request:
    :param experiment:
    :return: True - success, False - otherwise
    """
    status = query_emulab_instance_status(request, experiment)

    if status == '':
        logger.error('Do nothing since we cannot get the status from emulab')
        return False
    elif status != 'not_started':
        logger.warning('emulab experiment already started')
        logger.error('[testing code] Stopping emulab instance now, but we might want to move this stop to another button')
        return terminate_emulab_instance(request, experiment)

    # the status is 'not_started': create an instance of the API class
    # before that, make sure profile existed in emulab
    emulab_profile_name = get_emulab_profile_name(experiment.profile.project.name,
                                                  experiment.profile.name)
    if query_emulab_profile(request, emulab_profile_name) is None:
        create_new_emulab_profile(request, experiment.profile)

    api_instance = aerpawgw_client.ExperimentApi()
    location = 'RENCIEmulab'
    # location = experiment.reservation.location
    logger.error('[IMPORTANT] We should check if Reservation exists, and use that Reservation.location')
    logger.error('[IMPORTANT] now just hard-coded default: {}'.format(location))
    experiment_body = aerpawgw_client.Experiment(name=experiment.name,
                                                 profile=emulab_profile_name,
                                                 cluster=emulab_location_to_urn(location))
    experiment.key_inserted = False
    experiment.save()
    try:
        # create a experiment
        logger.warning(experiment_body)
        api_response = api_instance.create_experiment(experiment_body)
        logger.warning(api_response)
    except ApiException as e:
        logger.warning("Exception when calling ExperimentApi->create_experiment: %s\n" % e)
        return False

    return True


def query_emulab_instance_status(request, experiment):
    """
    Query the experiment instance status on Emulab

    :param request:
    :param experiment:
    :return status of emulab experiment: str, including 'not_started', 'provisioning',
                                             'provisioned', 'ready', 'failed'
    """
    if not os.getenv('AERPAWGW_HOST') \
            or not os.getenv('AERPAWGW_PORT') \
            or not os.getenv('AERPAWGW_VERSION'):
        return ''
    if experiment.profile is None or not is_emulab_profile(experiment.stage):
        return ''

    api_instance = aerpawgw_client.ExperimentApi()
    try:
        # get status of specific experiment
        emulab_experiment = api_instance.query_experiment(experiment.name)
        logger.warning('emulab_experiment:')
        logger.warning(emulab_experiment)
        logger.warning('experiment status on emulab: {}'.format(emulab_experiment.status))

        if emulab_experiment.status == 'ready' and not experiment.key_inserted:
            userid = request.user.username.split('@')[0]
            insert_user_to_emulab(request, userid, request.user.publickey, experiment)
            experiment.key_inserted = True
            experiment.save()
        return emulab_experiment.status
    except ApiException as e:
        logger.warning('experiment status on emulab: {}'.format('not_started'))
        return 'not_started'


def terminate_emulab_instance(request, experiment):
    """
    terminate the experiment instance on Emulab, the status has to be ready or failed.

    :param request:
    :param experiment:
    :return : True - success, False - try later
    """
    status = query_emulab_instance_status(request, experiment)

    if status == '':
        logger.error('Do nothing since we cannot get the status from emulab')
        return False
    elif status == 'not_started':
        return True
    elif status != 'ready' and status != 'failed':
        logger.error('The instance operation is in progress. Please try later.')
        return False
    api_instance = aerpawgw_client.ExperimentApi()
    try:
        # delete experiment
        api_instance.delete_experiment(experiment.name)
        experiment.key_inserted = False
        experiment.save()
    except ApiException as e:
        logger.warning("Exception when calling ExperimentApi->delete_experiment: %s\n" % e)
    return True


def get_non_emulab_manifest(request, experiment):
    """
    Send to script to aerpaw-gateway to parse and get the resources.

    :param request:
    :param experiment:
    :return : class Resource of aerpawgw_client. rspec and vnodes are what we need
    """
    # send to aerpaw-gateway to parse the script to get the resources
    api_instance = aerpawgw_client.ResourcesApi()
    body = aerpawgw_client.Profile(name='', script=experiment.profile.profile)
    logger.info(body)
    try:
        exp_resources = api_instance.parse_resources(body)
        for vnode in exp_resources.vnodes:
            # fill the IP and hostname info which is available at portal database
            # but not known by aerpaw-gateway
            # Use ('hardware_type': 'FixedNode', 'node': 'CC1') to find the resource
            resource = Resource.objects.get(resourceType=vnode.hardware_type, name=vnode.node)
            vnode.ipv4 = resource.ip_address
            vnode.hostname = resource.hostname
    except ApiException as e:
        logger.error("Exception when calling ResourcesApi->parse_resources: %s\n" % e)
        return None
    except ObjectDoesNotExist as e:
        logger.error("ObjectDoesNotExist: %s\n" % e)
        return None
    except:
        e = sys.exc_info()[0]
        logger.error("Exception getting resource: %s\n" % e)
        return None
    return exp_resources


def get_emulab_manifest(request, experiment):
    """
    Get manifest from Emulab, the status has to be ready.

    :param request:
    :param experiment:
    :return : class Resource of aerpawgw_client. rspec and vnodes are what we need
    """
    status = query_emulab_instance_status(request, experiment)
    if status != 'ready':
        return None
    api_instance = aerpawgw_client.ResourcesApi()
    try:
        exp_resources = api_instance.list_resources(experiment=experiment.name)
        logger.info(exp_resources)
    except ApiException as e:
        logger.error("Exception when calling ResourcesApi->list_resources: %s\n" % e)
        exp_resources = None
    return exp_resources


def insert_user_to_emulab(request, user, pubkey, experiment):
    """
    Insert user and pubkey to emulab instance.

    :param request:
    :param user: str
    :param pubkey: str
    :param experiment:
    :return: None
    """
    api_instance = aerpawgw_client.UserApi()
    body = aerpawgw_client.Userkey(user, pubkey)
    try:
        # add/update user and sshkey on experiment nodes
        logger.warning("insert user %s and public key to the instance\n" % user)
        api_instance.adduser(body, experiment.name)

    except ApiException as e:
        logger.error("Exception when calling UserApi->adduser: %s\n" % e)



'''
def get_emulab_instances(request):
    api_instance = aerpawgw_client.ExperimentApi()

    try:
        # get experiment(s) under user
        api_response = api_instance.get_experiments()
        logger.warning(api_response)
    except ApiException as e:
        logger.error("Exception when calling ExperimentApi->get_experiments: %s\n" % e)

    emulab_experiments = []
    for emulab_e in api_response:  # aerpawgw_client.models.experiment.Experiment
        e = Experiment()
        e.name = emulab_e.name
        e.created_date = datetime.fromtimestamp(int(emulab_e.start))
        e.created_by = request.user
        e.uuid = emulab_e.uuid

        # we need a field to store emulab eid (project+name)
        # borrow description field first.
        emulab_eid = '{},{}'.format(emulab_e.project, emulab_e.name)
        e.description = emulab_eid
        # e.emulab_eid = emulab_eid

        # e.project =
        # e.stage =
        emulab_experiments.append(e)

    return emulab_experiments
'''
