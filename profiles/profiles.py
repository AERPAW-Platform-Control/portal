import uuid

from django.utils import timezone

from .models import Profile
from accounts.models import AerpawUser
from projects.models import Project


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
    profile.save()

    profileer_id_list = form.data.getlist('profileer')
    update_profileer(profile, profileer_id_list)
    profile.save()

    try:
        profile.project = Project.objects.get(id=int(form.data.getlist('project')[0]))  
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
    profile.modified_by = request.user
    profile.modified_date = timezone.now()
    profile.save()
    return str(profile.uuid)

def delete_existing_profile(request, profile):
    """

    :param request:
    :param profile:
    :return:
    """
    try:
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