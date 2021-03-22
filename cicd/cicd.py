import uuid

from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from pprint import pprint

from .models import Cicd
from reservations.models import Reservation
from accounts.models import AerpawUser
from projects.models import Project
from profiles.models import Profile
from profiles.profiles import *
from resources.resources import *
import aerpawgw_client
from aerpawgw_client.rest import ApiException
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def get_cicd_list(request):
    """

    :param request:
    :return:
    """
    if request.user.is_superuser:
        cicds = Cicd.objects.order_by('name')
    else:
        cicds = Cicd.objects.filter(created_by=request.user).order_by('name')
    return cicds


def create_new_cicd(request, form):
    """

    :param request:
    :param form:
    :return:
    """
    pprint(form.data)
    cicd = Cicd()
    # base information
    cicd.uuid = uuid.uuid4()
    #request.session['experiment_uuid'] = experiment.uuid
    cicd.name = form.data.getlist('name')[0]
    try:
        cicd.description = form.data.getlist('description')[0]
        cicd.aerpaw_uuid = form.data.getlist('aerpaw_uuid')[0]
    except ValueError as e:
        print(e)
        cicd.description = None
        cicd.aerpaw_uuid = None
    # domain and port information
    cicd.fqdn_or_ip = form.data.getlist('fqdn_or_ip')[0]
    cicd.jenkins_slave_agent_port = form.data.getlist('jenkins_slave_agent_port')[0]
    cicd.jenkins_ssh_agent_port = form.data.getlist('jenkins_ssh_agent_port')[0]
    cicd.nginx_http_port = form.data.getlist('nginx_http_port')[0]
    cicd.nginx_https_port = form.data.getlist('nginx_https_port')[0]
    # admin information
    cicd.jenkins_admin_id = 'admin'
    cicd.jenkins_admin_name = form.data.getlist('jenkins_admin_name')[0]
    cicd.jenkins_admin_password = form.data.getlist('jenkins_admin_password')[0]
    # user information
    cicd.created_by = request.user
    cicd.modified_by = cicd.created_by
    # date information
    cicd.created_date = timezone.now()
    cicd.modified_date = cicd.created_date

    cicd.save()
    print(cicd)

    return str(cicd.uuid)


def update_existing_cicd(request, cicd, form):
    """
    Create new AERPAW Experiment

    :param request:
    :param form:
    :return:
    """
    try:
        cicd.modified_by = request.user
        cicd.modified_date = timezone.now()
        cicd.save()
    except ValueError as e:
        print(e)
    return str(cicd.uuid)