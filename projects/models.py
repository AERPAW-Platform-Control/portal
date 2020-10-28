import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from accounts.models import AerpawUser

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

    #experiments = models.ForeignKey(
    #    'experiments.Experiment', related_name='project_of_experiment', null=True, on_delete=models.SET_NULL
    #)

    class Meta:
        verbose_name = 'AERPAW Project'

    def __str__(self):
        return self.name



