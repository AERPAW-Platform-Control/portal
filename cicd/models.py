import uuid
from json import JSONEncoder
from uuid import UUID
from projects.models import Project

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from accounts.models import AerpawUser

JSONEncoder_olddefault = JSONEncoder.default
def JSONEncoder_newdefault(self, o):
    if isinstance(o, UUID): return str(o)
    return JSONEncoder_olddefault(self, o)
JSONEncoder.default = JSONEncoder_newdefault

User = get_user_model()

"""
aerpaw_uuid - from project uuid
fqdn_or_ip - from admin settings
jenkins_admin_id - from pi
jenkins_admin_password - from pi
jenkisn_admin_name - from pi
jenkins_slave_agent_port - from resource allocation
jenkins_ssh_agent_port - from resource allocation
fqdn_or_ip - fully qualified domain name or IP address
nginx_http_port - from resource allocation
nginx_https_port - from resource allocation
"""


class Cicd(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    # aerpaw_uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    aerpaw_uuid = models.CharField(max_length=255, default='')
    jenkins_admin_id = models.CharField(max_length=255, default='admin')
    jenkins_admin_password = models.CharField(max_length=255, default='password')
    jenkins_admin_name = models.CharField(max_length=255, default='admin')
    jenkins_slave_agent_port = models.IntegerField(default=50000)
    jenkins_ssh_agent_port = models.IntegerField(default=50022)
    fqdn_or_ip = models.CharField(max_length=255, default='127.0.0.1')
    nginx_http_port = models.IntegerField(default=8080)
    nginx_https_port = models.IntegerField(default=8443)
    created_by = models.ForeignKey(
        User, related_name='cicd_created_by', on_delete=models.CASCADE, null=True, blank=True
    )
    created_date = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey(
        User, related_name='cicd_modified_by', on_delete=models.CASCADE, null=True, blank=True
    )
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'AERPAW CICD'

    # def __str__(self):
    #     return self.name

    def __str__(self):
        return u'{0}'.format(self.name)



