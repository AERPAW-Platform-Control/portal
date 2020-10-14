from django.db import models

import uuid

from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts.models import AerpawUser
from projects.models import Project
from reservations.models import Reservation

# Create your models here.

class Experiment(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    stage = models.CharField(max_length=255)
    experimenter = models.ForeignKey(
        AerpawUser, related_name='experiment_experimenter', on_delete=models.CASCADE, null=True, blank=True
    )
    project = models.ForeignKey(
        Project, related_name='project_project', on_delete=models.CASCADE
    )
    profile = models.TextField()
    reservations = models.ForeignKey(
        Reservation, related_name='reservations', on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.name

