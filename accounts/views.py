# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import create_new_signup, update_credential
from .forms import AerpawUserSignupForm, AerpawUserCredentialForm
from django.http import FileResponse
import os, subprocess, tempfile
from zipfile import ZipFile


def profile(request):
    """

    :param request:
    :return:
    """
    user = request.user
    return render(request, 'profile.html', {'user': user})


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
                return redirect('profile')
            else:
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
