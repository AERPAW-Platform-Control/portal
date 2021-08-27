from uuid import uuid4

from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.utils import timezone

from usercomms.models import Usercomms
from accounts.models import AerpawUser


def portal_mail(subject, body_message, sender, receivers, reference_note='', reference_url=''):
    if receivers is None:
        receivers = []
    email_sender = settings.EMAIL_HOST_USER
    if sender == email_sender:
        sender = AerpawUser.objects.filter(is_superuser=True).first()
    email_uuid = uuid4()
    email_body = 'FROM: ' + str(sender.display_name) + \
                 '\r\nREQUEST: ' + str(reference_note) + \
                 '\r\n\r\nURL: ' + str(reference_url) + \
                 '\r\n\r\nMESSAGE: ' + body_message
    body = 'FROM: ' + str(sender.display_name) + \
           '\r\nREQUEST: ' + str(reference_note) + \
           '\r\nMESSAGE: ' + str(body_message)
    receivers_email = []
    for rc in receivers:
        receivers_email.append(rc.email)
    receivers = list(set(receivers))
    receivers_email = list(set(receivers_email))
    try:
        send_mail(subject, email_body, email_sender, receivers_email)
        created_by = sender
        created_date = timezone.now()
        # Sender
        uc = Usercomms(uuid=email_uuid, subject=subject, body=body, sender=created_by,
                       reference_url=None, reference_note=reference_note, reference_user=sender,
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
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
