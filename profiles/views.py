from django.shortcuts import render

# Create your views here.

from uuid import UUID

from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProfileCreateForm, ProfileUpdateForm
from .models import Profile
from .profiles import *


def profiles(request):
    """

    :param request:
    :return:
    """
    profiles = get_profile_list(request)
    return render(request, 'profiles.html', {'profiles': profiles})


def profile_create(request):
    """

    :param request:
    :return:
    """
    if request.method == "POST":
        form = ProfileCreateForm(request.POST, user=request.user)
        if form.is_valid():
            profile_uuid = create_new_profile(request, form)
            if profile_uuid is None:
                return render(request, 'profile_create.html', {'form': form,
                    'msg': '* Please check the experiment definition.'})
            return redirect('profile_detail', profile_uuid=profile_uuid)
    else:
        form = ProfileCreateForm(user=request.user)
    return render(request, 'profile_create.html', {'form': form})


def profile_detail(request, profile_uuid):
    """

    :param request:
    :param profile_uuid:
    :return:
    """
    profile = get_object_or_404(Profile, uuid=UUID(str(profile_uuid)))
    is_creator = (profile.created_by == request.user)
    return render(request, 'profile_detail.html',
    {'profile': profile, 'is_creator': is_creator})


def profile_update(request, profile_uuid):
    """

    :param request:
    :param profile_uuid:
    :return:
    """
    profile = get_object_or_404(Profile, uuid=UUID(str(profile_uuid)))
    if request.method == "POST":
        old_profile_name = profile.name
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            #if is_emulab_profile(profile):
            #    delete_emulab_profile(request, profile, old_profile_name)
            profile = form.save(commit=False)
            temporary_uuid = update_existing_profile(request, profile, form)
            if temporary_uuid is None:
                return render(request, 'profile_update.html',
                              { 'form': form, 'profile_uuid': str(profile_uuid), 'profile_name': profile.name,
                                'msg': '* Please check the experiment definition.'}
                              )
            else:
                return redirect('profile_detail', profile_uuid=str(profile.uuid))
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'profile_update.html',
                  {
                      'form': form, 'profile_uuid': str(profile_uuid), 'profile_name': profile.name}
                  )


def profile_delete(request, profile_uuid):
    """

    :param request:
    :param profile_uuid:
    :return:
    """
    profile = get_object_or_404(Profile, uuid=UUID(str(profile_uuid)))
    if request.method == "POST":
        is_removed = delete_existing_profile(request, profile)
        if is_removed:
            return redirect('profiles')
    return render(request, 'profile_delete.html', {'profile': profile})
