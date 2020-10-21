import uuid

from django.utils import timezone

from .models import Resource
from accounts.models import AerpawUser


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

    resource.resourceType = form.data.getlist('units')[0]

    resource.location = form.data.getlist('location')[0]

    resource.save()
    return str(resource.uuid)


def update_resource_resources(resource, resource_resource_id_list):
    """

    :param resource:
    :param resource_resource_id_list:
    :return:
    """
    # clear current resource resource
    resource.resource_resources.clear()
    # add members from resource_member_id_update_list
    for resource_id in resource_resource_id_list:
        resource_resource = AerpawUser.objects.get(id=int(resource_id))
        resource.resource_resources.add(resource_resource)
    resource.save()
    # add principal_investigator to resource_members if not already there
    if resource.resource not in resource.resource_resources.all():
        resource.resource_resources.add(resource.resource)
        resource.save()


def update_existing_resource(request, resource, form):
    """
    Create new AERPAW resource

    :param request:
    :param form:
    :return:
    """
    resource.modified_by = request.user
    resource.modified_date = timezone.now()
    resource.save()
    resource_member_id_list = form.data.getlist('resource_resources')
    update_resource_resources(resource, resource_resource_id_list)
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