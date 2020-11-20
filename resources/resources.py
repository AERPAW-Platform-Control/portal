import uuid

from django.utils import timezone
from datetime import datetime,timedelta
from django.db.models import Q

from .models import Resource
from accounts.models import AerpawUser
from reservations.models import Reservation,ReservationStatusChoice


def create_new_resource(request, form):
    """

    :param request:
    :param form:
    :return:
    """
    resource = Resource()
    resource.uuid = uuid.uuid4()
    resource.name = form.data.getlist('name')[0]
    try:
        resource.description = form.data.getlist('description')[0]
    except ValueError as e:
        print(e)
        resource.description = None

    resource.resourceType = form.data.getlist('resourceType')[0]

    resource.units = form.data.getlist('units')[0]

    resource.location = form.data.getlist('location')[0]

    resource.save()
    return str(resource.uuid)

def update_existing_resource(request, resource, form):
    """
    Create new AERPAW resource

    :param request:
    :param form:
    :return:
    """
    resource.name = form.data.getlist('name')[0]
    try:
        resource.description = form.data.getlist('description')[0]
    except ValueError as e:
        print(e)
        resource.description = None

    resource.resourceType = form.data.getlist('resourceType')[0]

    resource.units = form.data.getlist('units')[0]

    resource.location = form.data.getlist('location')[0]
    resource.modified_by = request.user
    resource.modified_date = timezone.now()
    resource.save()
    return str(resource.uuid)


def delete_existing_resource(request, resource):
    """

    :param request:
    :param resource:
    :return:
    """
    try:
        resource.delete()
        return True
    except Exception as e:
        print(e)
    return False


def get_resource_list(request):
    """

    :param request:
    :return:
    """
    if request.user.is_superuser:
        resources = Resource.objects.order_by('name')
    else:
        resources = Resource.objects.order_by('name')
    return resources

def get_reserved_resource(start_time,end_time):
    resources = Resource.objects.order_by('name')
    resource_units={}
    for resource in resources:
        reserved_units=get_reserved_units(resource,start_time,end_time)
        available_units=resource.units-reserved_units
        units=[]
        units.append(reserved_units)
        units.append(available_units)
        resource_units[resource.uuid] = units
    return resource_units

def get_all_reserved_units(term,delta):
    start_time = datetime.today()
    all_units={}
    for i in range(term):
        end_time = start_time + timedelta(hours=delta)
        reserved_units = get_reserved_resource(start_time,end_time)
        start_time=end_time
        all_units[i] = reserved_units
    return all_units

def is_resource_available_time(resource, start_time,end_time):
    if not resource.is_units_available():
        return False
    print("oookkkk")
    print(start_time)
    print(end_time)
    reserved_units = get_reserved_units(resource,start_time,end_time)
    return resource.is_units_available_reservation(reserved_units)

def get_reserved_units(resource,start,end):
    qs0 = Reservation.objects.filter(state=ReservationStatusChoice.SUCCESS.value)
    qs1 = qs0.filter(start_date__lte=end)
    qs2 = qs1.filter(end_date__gte=end)
    qs3= qs2.filter(resource = resource)
    units=0
    for rs in qs3:
        units+=rs.units
    return units