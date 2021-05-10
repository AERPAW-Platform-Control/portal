# accounts/views.py

import os
import subprocess
import tempfile
from zipfile import ZipFile

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render, redirect

from .accounts import create_new_role_request
from .forms import AerpawUserSignupForm, AerpawUserCredentialForm, AerpawRoleRequestForm, AerpawUser
from .models import create_new_signup, update_credential


@login_required
def profile(request):
    """

    :param request:
    :return:
    """
    user = request.user
    if request.method == 'POST':
        for key in request.POST.keys():
            if not key == 'csrfmiddlewaretoken':
                display_name = request.POST.get(key)
                if len(display_name) < 5:
                    messages.error(request, 'ERROR: Display Name must be at least 5 characters long...')
                    return render(request, 'profile.html', {'user': user})
                user_obj = AerpawUser.objects.get(id=user.id)
                if user_obj.display_name != display_name:
                    user_obj.display_name = display_name
                    user_obj.save()
                    user = user_obj

    return render(request, 'profile.html', {'user': user})


@login_required
def request_roles(request):
    """

    :param request:
    :return:
    """
    if request.method == "POST":
        form = AerpawRoleRequestForm(request.POST, user=request.user)
        if form.is_valid():
            # signup_uuid = create_new_signup(request, form)
            role_request = create_new_role_request(request, form)
            messages.info(request, 'INFO: Role Request has been created for - {0}'.format(str(role_request)))
            return redirect('profile')
    else:
        form = AerpawRoleRequestForm(user=request.user)
    return render(request, 'request_roles.html', {'form': form})


@login_required
def signup(request):
    """

    :param request:
    :return:
    """

    if request.method == "POST":
        form = AerpawUserSignupForm(request.POST)
        if form.is_valid():
            signup_uuid = create_new_signup(request, form)
            return redirect('home')
    else:
        form = AerpawUserSignupForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def credential(request):
    """

    :param request:
    :return:
    """

    if request.method == "POST":
        form = AerpawUserCredentialForm(request.POST)
        if 'savebtn' in request.POST and form.is_valid():
            if request.POST['publickey']:
                update_credential(request, form)
                form = AerpawUserCredentialForm() # clear form
            render(request, 'credential.html', {'form': form})

        elif 'generatebtn' in request.POST:
            keyfile = os.path.join(tempfile.gettempdir(), 'aerpaw_id_rsa')
            args = "ssh-keygen -q -t rsa -N '' -C {} -f {}".format(request.user.username,
                                                                   keyfile).split()
            args[5] = ''  # make passphrase empty (the parameter for -N)
            ret = subprocess.run(args, check=True)
            # print(ret)
            try:
                with ZipFile(os.path.join(tempfile.gettempdir(), 'aerpaw_id_rsa.zip'),
                             'w') as myzip:
                    myzip.write(keyfile + '.pub', arcname='aerpaw_id_rsa.pub')
                    myzip.write(keyfile, arcname='aerpaw_id_rsa')
            except:
                print('something wrong with zipfile')

            os.unlink(keyfile)
            os.unlink(keyfile + '.pub')
            return FileResponse(
                open(os.path.join(tempfile.gettempdir(), 'aerpaw_id_rsa.zip'), 'rb'),
                as_attachment=True)
    else:
        form = AerpawUserCredentialForm()
    return render(request, 'credential.html', {'form': form})
