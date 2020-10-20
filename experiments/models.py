from django.db import models

import uuid

from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts.models import AerpawUser
from projects.models import Project
#from reservations.models import Reservation

# Create your models here.

class Experiment(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    stage = models.CharField(max_length=255)
    experimenter = models.ManyToManyField(
        AerpawUser, related_name='experiment_experimenter'
    )
    project = models.ForeignKey(
        Project, related_name='experiment_project', on_delete=models.CASCADE
    )

    #created_by = experiment_project.created_by
    created_date = models.DateTimeField(default=timezone.now)
    
    #modified_by = experiment_project.modified_by
    modified_date = models.DateTimeField(blank=True, null=True)

    #reservations = models.ForeignKey(
    #    Reservation, related_name='experiment_reservations', on_delete=models.CASCADE, null=True, blank=True
    #)

    class Meta:
        verbose_name = 'AERPAW Experiment'

    def __str__(self):
        return self.name

