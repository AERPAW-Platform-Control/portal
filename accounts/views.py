import os
import subprocess
import tempfile
from uuid import uuid4
from zipfile import ZipFile

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.http import FileResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from usercomms.models import Usercomms
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
    if request.method == 'GET':
        form = AerpawRoleRequestForm(user=request.user)
    else:
        form = AerpawRoleRequestForm(request.POST, user=request.user)
        if form.is_valid():
            email_uuid = uuid4()
            role_request = create_new_role_request(request, form)
            reference_note = 'Add role ' + str(role_request)
            reference_url = 'https://' + str(request.get_host()) + '/manage/user_requests'
            subject = '[AERPAW] Request to add role ' + str(role_request)
            sender = settings.EMAIL_HOST_USER
            body = 'FROM: ' + request.user.display_name + \
                   '\r\nREQUEST: ' + reference_note + \
                   '\r\n\r\nPURPOSE: ' + form.cleaned_data['purpose']
            email_body = 'FROM: ' + request.user.display_name + \
                         '\r\nREQUEST: ' + reference_note + \
                         '\r\n\r\nURL: ' + reference_url + \
                         '\r\n\r\nPURPOSE: ' + form.cleaned_data['purpose']
            receivers = []
            receivers_email = []
            user_managers = AerpawUser.objects.filter(groups__name='user_manager')
            for um in user_managers:
                receivers.append(um)
                receivers_email.append(um.email)
            receivers = list(set(receivers))
            receivers_email = list(set(receivers_email))

            print(receivers)
            print(receivers_email)
            try:
                send_mail(subject, email_body, sender, receivers_email)
                # Sender
                created_by = request.user
                created_date = timezone.now()
                uc = Usercomms(uuid=email_uuid, subject=subject, body=body, sender=created_by,
                               reference_url=None, reference_note=None, reference_user=created_by,
                               created_by=created_by, created_date=created_date)
                uc.save()
                for rc in receivers:
                    uc.receivers.add(rc)
                uc.save()
                # Receivers
                for rc in receivers:
                    uc = Usercomms(uuid=email_uuid, subject=subject, body=email_body, sender=created_by,
                                   reference_url=reference_url, reference_note=reference_note, reference_user=rc,
                                   created_by=created_by, created_date=created_date)
                    uc.save()
                    for inner_rc in receivers:
                        uc.receivers.add(inner_rc)
                    uc.save()
                messages.info(request, 'Success! Request to add role: ' + str(role_request) + ' has been sent')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('profile')

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
                form = AerpawUserCredentialForm()  # clear form
            render(request, 'credential.html', {'form': form})

        elif 'generatebtn' in request.POST:
            keyfile = os.path.join(tempfile.gettempdir(), 'aerpaw_id_rsa')
            args = "ssh-keygen -q -t rsa -N '' -C {} -f {}".format(request.user.username,
                                                                   keyfile).split()
            args[5] = ''  # make passphrase empty (the parameter for -N)
            try:
                output = subprocess.run(args, check=False, capture_output=True)
                with ZipFile(os.path.join(tempfile.gettempdir(), 'aerpaw_id_rsa.zip'),
                             'w') as myzip:
                    myzip.write(keyfile + '.pub', arcname='aerpaw_id_rsa.pub')
                    myzip.write(keyfile, arcname='aerpaw_id_rsa')
                os.unlink(keyfile)
                os.unlink(keyfile + '.pub')
                return FileResponse(
                    open(os.path.join(tempfile.gettempdir(), 'aerpaw_id_rsa.zip'), 'rb'),
                    as_attachment=True)
            except Exception as e:
                print(output)
                print(e)
    else:
        form = AerpawUserCredentialForm()
    return render(request, 'credential.html', {'form': form})
