from django.db import models

import uuid
from enum import Enum
from django.contrib.auth import get_user_model
from django.utils import timezone


from accounts.models import AerpawUser
from projects.models import Project
from resources.models import ResourceStageChoice
#from reservations.models import Reservation

class ReservationStateChoice(Enum):   # A subclass of Enum
    IDLE = 'Idle'
    SUCCESS = 'Success'
    FAILURE = 'Failure'
    RETRY = 'Retry'
    EXPIRATION = 'Expiration'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

# Create your models here.

class Experiment(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()

    experimenter = models.ManyToManyField(
        AerpawUser, related_name='experiment_experimenter'
    )
    project = models.ForeignKey(
        Project, related_name='experiment_project', on_delete=models.CASCADE
    )

    created_by = models.ForeignKey(
        AerpawUser, related_name='experiment_created_by', null=True, on_delete=models.SET_NULL
    )
    created_date = models.DateTimeField(default=timezone.now)
    
    modified_by = models.ForeignKey(
        AerpawUser, related_name='experiment_modified_by', null=True, on_delete=models.SET_NULL
    )
    modified_date = models.DateTimeField(blank=True, null=True)

    stage=models.CharField(
      max_length=64,
      choices=ResourceStageChoice.choices(),
    )

    #reservations = models.ForeignKey(
    #    Reservation, related_name='experiment_reservations', on_delete=models.CASCADE, null=True, blank=True
    #)

    class Meta:
        verbose_name = 'AERPAW Experiment'

    def __str__(self):
        return self.name

