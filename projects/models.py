import uuid
from json import JSONEncoder
from uuid import UUID

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

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    principal_investigator = models.ForeignKey(
        AerpawUser, related_name='project_principal_investigator', on_delete=models.CASCADE
    )
    project_members = models.ManyToManyField(
        AerpawUser, related_name='projects'
    )
    created_by = models.ForeignKey(
        User, related_name='project_created_by', on_delete=models.CASCADE, null=True, blank=True
    )
    created_date = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey(
        User, related_name='project_modified_by', on_delete=models.CASCADE, null=True, blank=True
    )
    modified_date = models.DateTimeField(blank=True, null=True)

    experiments = models.ForeignKey(
        'experiments.Experiment', related_name='project_of_experiment', null=True, on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = 'AERPAW Project'

    # def __str__(self):
    #     return self.name

    def __str__(self):
        return u'{0}'.format(self.name)



