# Create your views here.

# Create your views here.

from django.contrib.auth.decorators import user_passes_test

from uuid import UUID

from django.shortcuts import render, redirect, get_object_or_404

from .forms import ResourceCreateForm, ResourceChangeForm
from .models import Resource
from .resources import create_new_resource, get_resource_list, update_existing_resource, delete_existing_resource, get_all_reserved_units


def resources(request):
    """

    :param request:
    :return:
    """
    resources = get_resource_list(request)
    reserved_resource = get_all_reserved_units()
    return render(request, 'resources.html', {'resources': resources, 'reservations': reserved_resource})

@user_passes_test(lambda u: u.is_superuser)
def resource_create(request):
    """

    :param request:
    :return:
    """
    if request.method == "POST":
        form = ResourceCreateForm(request.POST)
        if form.is_valid():
            resource_uuid = create_new_resource(request, form)
            return redirect('resource_detail', resource_uuid=resource_uuid)
    else:
        form = ResourceCreateForm()
    return render(request, 'resource_create.html', {'form': form})


def resource_detail(request, resource_uuid):
    """

    :param request:
    :param resource_uuid:
    :return:
    """
    resource = get_object_or_404(Resource, uuid=UUID(str(resource_uuid)))
    resource_reservations = resource.reservation_of_resource
    return render(request, 'resource_detail.html', {'resource': resource}, {'reservations': resource_reservations.all()})


def resource_update(request, resource_uuid):
    """

    :param request:
    :param resource_uuid:
    :return:
    """
    resource = get_object_or_404(Resource, uuid=UUID(str(resource_uuid)))
    if request.method == "POST":
        form = ResourceChangeForm(request.POST, instance=resource)
        if form.is_valid():
            resource = form.save(commit=False)
            resource_uuid = update_existing_resource(request, resource, form)
            return redirect('resource_detail', resource_uuid=str(resource.uuid))
    else:
        form = ResourceChangeForm(instance=resource)
    return render(request, 'resource_update.html',
                  {
                      'form': form, 'resource_uuid': str(resource_uuid), 'resource_name': resource.name}
                  )


def resource_delete(request, resource_uuid):
    """

    :param request:
    :param resource_uuid:
    :return:
    """
    resource = get_object_or_404(Resource, uuid=UUID(str(resource_uuid)))
    if request.method == "POST":
        is_removed = delete_existing_resource(request, resource)
        if is_removed:
            return redirect('resources')
    return render(request, 'resource_delete.html', {'resource': resource})
