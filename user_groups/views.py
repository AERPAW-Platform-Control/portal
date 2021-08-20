from uuid import uuid4

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from accounts.models import AerpawUser, AerpawRoleRequest
from usercomms.models import Usercomms
from .templatetags.user_groups import role_name


@login_required
def user_groups(request):
    """

    :param request:
    :return:
    """
    if request.method == 'POST':
        for key in request.POST.keys():
            if not key == 'csrfmiddlewaretoken':
                cur_value = request.POST.get(key)
                parse_key = key.rsplit('_', 1)
                user_obj = AerpawUser.objects.get(id=int(parse_key[1]))
                group_obj = Group.objects.get(name=parse_key[0])
                if str(cur_value) == 'True':
                    user_obj.groups.remove(group_obj)
                else:
                    user_obj.groups.add(group_obj)
                user_obj.save()
    user = request.user
    all_users = AerpawUser.objects.all().exclude(username='admin').order_by('username')
    return render(request, 'user_groups.html', {'user': user, 'all_users': all_users})


@login_required
def user_requests(request):
    """

    :param request:
    :return:
    """
    if request.method == "POST":
        for key in request.POST.keys():
            if not key == 'csrfmiddlewaretoken':
                parse_key = key.rsplit('_', 1)
                if parse_key[0] != 'notes':
                    role = parse_key[0]
                    role_request = AerpawRoleRequest.objects.get(id=int(parse_key[1]))
                    notes = request.POST.get('notes_' + str(parse_key[1]))
                    if request.POST.get(key) == 'Approve':
                        is_approved = True
                    else:
                        is_approved = False
        # get user_obj
        user_obj = AerpawUser.objects.get(id=int(role_request.requested_by_id))
        group_obj = Group.objects.get(name=str(role))
        r_name = role_name(group_obj.name)
        if str(is_approved) == 'True':
            user_obj.groups.add(group_obj)
        else:
            user_obj.groups.remove(group_obj)
        user_obj.save()
        role_request.notes = notes
        role_request.is_approved = is_approved
        role_request.is_completed = True
        role_request.save()
        # TODO: email
        email_uuid = uuid4()
        reference_note = 'Add role ' + r_name
        reference_url = 'https://' + str(request.get_host()) + '/manage/user_requests'
        if is_approved:
            subject = '[AERPAW] Request to add role ' + r_name + ' is APPROVED'
        else:
            subject = '[AERPAW] Request to add role ' + r_name + ' is DENIED'
        email_sender = settings.EMAIL_HOST_USER
        body = 'FROM: ' + request.user.display_name + \
               '\r\nREQUEST: ' + reference_note + \
               '\r\n\r\nMESSAGE: ' + notes
        email_body = 'FROM: ' + request.user.display_name + \
                     '\r\nREQUEST: ' + reference_note + \
                     '\r\n\r\nURL: ' + reference_url + \
                     '\r\n\r\nMESSAGE: ' + notes
        receivers = [user_obj]
        receivers_email = [user_obj.email]
        try:
            send_mail(subject, body, email_sender, receivers_email)
            # Sender
            created_by = request.user
            created_date = timezone.now()
            uc = Usercomms(uuid=email_uuid, subject=subject, body=email_body, sender=created_by,
                           reference_url=None, reference_note=None, reference_user=created_by,
                           created_by=created_by, created_date=created_date)
            uc.save()
            for rc in receivers:
                uc.receivers.add(rc)
            uc.save()
            # Receivers
            for rc in receivers:
                uc = Usercomms(uuid=email_uuid, subject=subject, body=body, sender=created_by,
                               reference_url=reference_url, reference_note=reference_note, reference_user=rc,
                               created_by=created_by, created_date=created_date)
                uc.save()
                for inner_rc in receivers:
                    uc.receivers.add(inner_rc)
                uc.save()
            if is_approved:
                messages.info(request, 'Success! Role request: ' + r_name + ' has been APPROVED')
            else:
                messages.info(request, 'Success! Role request: ' + r_name + ' has been DENIED')
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

    open_u_reqs = AerpawRoleRequest.objects.filter(is_completed=False).order_by('-created_date')
    closed_u_reqs = AerpawRoleRequest.objects.filter(is_completed=True).order_by('-created_date')
    return render(request, 'user_requests.html', {'ou_reqs': open_u_reqs, 'cu_reqs': closed_u_reqs})
