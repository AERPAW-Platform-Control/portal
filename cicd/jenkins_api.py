from uuid import UUID
import jenkins
from . import jenkins_server as js
from .models import Cicd
from django.shortcuts import render, redirect, get_object_or_404
from pprint import pprint
from jenkins import JenkinsException

from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

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

# logger = logging.getLogger(__name__)
#
# # TODO: pull username/password from admin config for operator ci/cd deployment
# jenkins_server = jenkins.Jenkins(
#     'https://aerpaw-ci.renci.org/jenkins',
#     username='admin',
#     password='xxxxxxx'
# )
# jenkins_server._session.verify = False

# params = { \
#     'AERPAW_UUID': 'a355f97e-2ccf-4d53-9821-6c3099193e97', \
#     'FQDN_OR_IP': 'aerpaw-dev.renci.org', \
#     'JENKINS_ADMIN_ID': 'admin', \
#     'JENKINS_ADMIN_NAME': 'TEST Admin', \
#     'JENKINS_ADMIN_PASSWORD': 'password123!', \
#     'JENKINS_SLAVE_AGENT_PORT': '50001', \
#     'JENKINS_SSH_AGENT_PORT': '50023', \
#     'NGINX_HTTP_PORT': '9090', \
#     'NGINX_HTTPS_PORT': '9443' \
#  \
#     }


def deploy_cicd_environment(cicd_uuid):
    cicd = get_object_or_404(Cicd, uuid=UUID(str(cicd_uuid)))
    params = {
        'AERPAW_UUID': str(cicd.uuid),
        'AERPAW_COMMAND': 'DEPLOY',
        'FQDN_OR_IP': str(cicd.fqdn_or_ip),
        'JENKINS_ADMIN_ID': str(cicd.jenkins_admin_id),
        'JENKINS_ADMIN_NAME': str(cicd.jenkins_admin_name),
        'JENKINS_ADMIN_PASSWORD': str(cicd.jenkins_admin_password),
        'JENKINS_SLAVE_AGENT_PORT': str(cicd.jenkins_slave_agent_port),
        'JENKINS_SSH_AGENT_PORT': str(cicd.jenkins_ssh_agent_port),
        'NGINX_HTTP_PORT': str(cicd.nginx_http_port),
        'NGINX_HTTPS_PORT': str(cicd.nginx_https_port)
        }
    next_bn = js.get_job_info('manage-aerpaw-cicd')['nextBuildNumber']
    output = js.build_job('manage-aerpaw-cicd', parameters=params)
    # print(output)
    return next_bn


def start_cicd_environment(cicd_uuid):
    params = {
        'AERPAW_UUID': cicd_uuid,
        'AERPAW_COMMAND': 'START'
    }
    print(params)
    next_bn = js.get_job_info('manage-aerpaw-cicd')['nextBuildNumber']
    output = js.build_job('manage-aerpaw-cicd', parameters=params)
    # print(output)
    # info = js.get_build_console_output('aerpaw-cicd-control', next_bn)
    # pprint(info)
    return next_bn


def stop_cicd_environment(cicd_uuid):
    params = {
        'AERPAW_UUID': cicd_uuid,
        'AERPAW_COMMAND': 'STOP'
    }
    print(params)
    next_bn = js.get_job_info('manage-aerpaw-cicd')['nextBuildNumber']
    output = js.build_job('manage-aerpaw-cicd', parameters=params)
    # print(output)
    # info = js.get_build_console_output('aerpaw-cicd-control', next_bn)
    # pprint(info)
    return next_bn


def purge_cicd_environment(cicd_uuid):
    params = {
        'AERPAW_UUID': cicd_uuid,
        'AERPAW_COMMAND': 'PURGE'
    }
    print(params)
    next_bn = js.get_job_info('manage-aerpaw-cicd')['nextBuildNumber']
    output = js.build_job('manage-aerpaw-cicd', parameters=params)
    # print(output)
    # info = js.get_build_console_output('aerpaw-cicd-control', next_bn)
    # pprint(info)
    return next_bn


def info_cicd_environment(cicd_uuid):
    next_bn = js.get_job_info('manage-aerpaw-cicd')['nextBuildNumber']
    # output = js.build_job('manage-aerpaw-cicd', parameters=params)
    try:
        info = js.get_build_console_output('aerpaw-cicd-control', int(next_bn - 1))
        response = '[job #{0}]: '.format(str(next_bn - 1)) + "<br />".join(info.split("\n"))
    except JenkinsException as err:
        print(err)
        response = '[job #?]: Unable to locate job'
    # pprint(info)

    # print(response)
    return response
