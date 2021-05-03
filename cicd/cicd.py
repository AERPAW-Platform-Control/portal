import uuid

from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from pprint import pprint

from .models import Cicd, CicdHostInfo
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
        user_id = AerpawUser.objects.filter(username=request.user.username).values('id')[0]['id']
        print(user_id)
        cicds = Cicd.objects.filter(created_by_id=int(user_id)).order_by('name')
        print(cicds)
    return cicds


def get_cicd_host_info_list(request):
    """

    :param request:
    :return:
    """
    if request.user.is_superuser:
        cicd_his = CicdHostInfo.objects.order_by('name')
    else:
        cicd_his = CicdHostInfo.objects.filter(created_by=request.user).order_by('name')
    return cicd_his


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
    cicd.cicd_host_info = CicdHostInfo.objects.get(id=int(form.data.getlist('cicd_host')[0]))
    #cicd.fqdn_or_ip = form.data.getlist('fqdn_or_ip')[0]
    #cicd.jenkins_service_agent_port = form.data.getlist('jenkins_service_agent_port')[0]
    #cicd.jenkins_ssh_agent_port = form.data.getlist('jenkins_ssh_agent_port')[0]
    #cicd.nginx_http_port = form.data.getlist('nginx_http_port')[0]
    #cicd.nginx_https_port = form.data.getlist('nginx_https_port')[0]
    # admin information
    cicd.jenkins_admin_id = 'projectpi'
    cicd.jenkins_admin_name = request.user.username
    cicd.jenkins_admin_password = form.data.getlist('jenkins_admin_password')[0]
    # user information
    cicd.created_by = request.user
    cicd.modified_by = cicd.created_by
    # date information
    cicd.created_date = timezone.now()
    cicd.modified_date = cicd.created_date
    cicd.save()
    # update cicd_host_info object as allocated
    cicd_hi = CicdHostInfo.objects.get(id=int(form.data.getlist('cicd_host')[0]))
    cicd_hi.is_allocated = True
    cicd_hi.save()
    print(cicd)

    return str(cicd.uuid)


def create_new_cicd_host_info(request, form):
    """

    :param request:
    :param form:
    :return:
    """
    pprint(form.data)
    cicd_hi = CicdHostInfo()
    # base information
    cicd_hi.uuid = uuid.uuid4()
    #request.session['experiment_uuid'] = experiment.uuid
    cicd_hi.name = form.data.getlist('name')[0]
    try:
        cicd_hi.description = form.data.getlist('description')[0]
    except ValueError as e:
        print(e)
        cicd_hi.description = None
    # domain and port information
    cicd_hi.fqdn_or_ip = form.data.getlist('fqdn_or_ip')[0]
    cicd_hi.docker_subnet = form.data.getlist('docker_subnet')[0]
    cicd_hi.jenkins_service_agent_port = form.data.getlist('jenkins_service_agent_port')[0]
    cicd_hi.jenkins_ssh_agent_port = form.data.getlist('jenkins_ssh_agent_port')[0]
    cicd_hi.gitea_ssh_agent_port = form.data.getlist('gitea_ssh_agent_port')[0]
    cicd_hi.nginx_http_port = form.data.getlist('nginx_http_port')[0]
    cicd_hi.nginx_https_port = form.data.getlist('nginx_https_port')[0]
    # user information
    cicd_hi.created_by = request.user
    cicd_hi.modified_by = cicd_hi.created_by
    # date information
    cicd_hi.created_date = timezone.now()
    cicd_hi.modified_date = cicd_hi.created_date

    cicd_hi.save()
    print(cicd_hi)

    return str(cicd_hi.uuid)


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