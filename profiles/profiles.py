import uuid
import os
from django.utils import timezone

from .models import Profile
from accounts.models import AerpawUser
from projects.models import Project
import aerpawgw_client
from aerpawgw_client.rest import ApiException
import logging

logger = logging.getLogger(__name__)


def create_new_profile(request, form):
    """

    :param request:
    :param form:
    :return:
    """
    profile = Profile()
    profile.uuid = uuid.uuid4()
    request.session['profile_uuid'] = profile.uuid
    profile.name = form.data.getlist('name')[0]

    try:
        profile.description = form.data.getlist('description')[0]
    except ValueError as e:
        print(e)
        profile.description = None

    try:
        profile.profile = form.data.getlist('profile')[0]
    except ValueError as e:
        print(e)
        profile.profile = None

    profile.created_by = request.user
    profile.created_date = timezone.now()
    profile.project = Project.objects.get(id=int(form.data.getlist('project')[0]))
    profile.stage = form.data.getlist('stage')[0]

    # not every profile need to be sent to emulab,
    # now in is_emulab_profile(), using Stage 'DEVELOPMENT' to see if it's for emulab
    if is_emulab_profile(profile.stage):
        create_new_emulab_profile(request, profile)

    profile.save()
    try:
        profile.project.profile_of_project.add(profile)
        profile.save()
    except ValueError as e:
        print(e)
        profile.project = None

    #try:
    #    reservation_id_list=form.data.getlist('reservation')
    #    if not reservation_id_list:
    #        reservation_id = reservation_id_list[0]
    #        profile.reservations = Reservation.objects.get(id=int(reservation_id))
    #except ValueError as e:
    #    print(e)
    #    profile.reservations= None
    #profile.save()

    return str(profile.uuid)


def update_existing_profile(request, profile, form):
    """
    Create new AERPAW Profile

    :param request:
    :param form:
    :return:
    """
    try:
        profile.description = form.data.getlist('description')[0]
    except ValueError as e:
        profile.description = None
    profile.modified_by = request.user
    profile.modified_date = timezone.now()

    if is_emulab_profile(profile.stage):
        delete_emulab_profile(request, profile)
        create_new_emulab_profile(request, profile)

    profile.save()
    return str(profile.uuid)


def delete_existing_profile(request, profile):
    """

    :param request:
    :param profile:
    :return:
    """
    try:
        if is_emulab_profile(profile.stage):
            delete_emulab_profile(request, profile)
        profile.delete()
        return True
    except Exception as e:
        print(e)
    return False


def get_profile_list(request):
    """

    :param request:
    :return:
    """
    if request.user.is_superuser:
        profiles = Profile.objects.order_by('name')
    else:
        profiles = Profile.objects.order_by('name')
    return profiles


def is_emulab_profile(stage):
    # not every profile need to be sent to emulab,
    # first check if we have AERPAWGW env setup,
    # and check the Stage 'DEVELOPMENT' to see if it's for emulab
    if not os.getenv('AERPAWGW_HOST') \
            or not os.getenv('AERPAWGW_PORT') \
            or not os.getenv('AERPAWGW_VERSION'):
        return False
    elif stage.upper() == 'DEVELOPMENT':
        return True
    else:
        return False


def query_emulab_profile(request, emulab_profile_name):
    """
    Query emulab profile

    :param request: in case we need user info later
    :param emulab_profile_name:
    :return emulab_profile:
    """
    api_instance = aerpawgw_client.ProfileApi()
    print(emulab_profile_name)
    try:
        # query specific profile
        emulab_profile = api_instance.query_profile(profile=emulab_profile_name)
        print(emulab_profile)
        return emulab_profile
    except ApiException as e:
        print("Exception when calling ProfileApi->query_profile: %s\n" % e)
        return None


def create_new_emulab_profile(request, profile):
    """
    Create new Profile on Emulab

    :param request: in case we need user info later
    :param profile:
    :return:
    """
    emulab_profile_name = get_emulab_profile_name(profile.project.name, profile.name)

    # create on emulab
    api_instance = aerpawgw_client.ProfileApi()
    body = aerpawgw_client.Profile(name=emulab_profile_name, script=profile.profile)
    logger.debug(body)
    try:
        api_response = api_instance.create_profile(body)
        print(api_response)
    except ApiException as e:
        raise Exception("Exception when calling Gateway->create_profile: %s\n" % e)

    # verify created profile on emulab by querying it
    try:
        profile_created = query_emulab_profile(request, emulab_profile_name)
        if profile_created is None:
            raise Exception("failed to query the created emulab profile")
    except Exception as e:
        raise Exception("failed to query the created emulab profile")


def delete_emulab_profile(request, profile, name_to_delete=None):
    """
    Delte profile in emulab cloud

    :param request: in case we need user info later
    :param profile:
    :param name_to_delete: in case of user updates the name in profile,
                            we will need to use the oldnname to delete
    :return
    """
    if name_to_delete is None:
        emulab_profile_name = get_emulab_profile_name(profile.project.name, profile.name)
    else:
        emulab_profile_name = get_emulab_profile_name(profile.project.name, name_to_delete)
    api_instance = aerpawgw_client.ProfileApi()
    try:
        # delete profile
        api_instance.delete_profile(emulab_profile_name)
    except ApiException as e:
        print("Exception when calling ProfileApi->delete_profile: %s\n" % e)


def get_emulab_profile_name(projectname, profilename):
    return '{}-{}'.format(projectname, profilename)
