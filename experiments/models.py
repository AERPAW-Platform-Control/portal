from django.db import models

import uuid
from enum import Enum
from django.contrib.auth import get_user_model
from django.utils import timezone


from accounts.models import AerpawUser
from projects.models import Project
from resources.models import ResourceStageChoice
from profiles.models import Profile


class StageChoice(Enum):   # A subclass of Enum
    IDLE = 'Idle'
    DEVELOPMENT = 'Development'
    SANDBOX = 'Sandbox'
    SANDBOXRequest = 'SandboxRequest'
    EMULATION = 'Emulation'
    EMULATIONRequest = 'EmulationRequest'
    TESTBED = 'Testbed'
    TESTBEDRequest = 'TestbedRequest'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ResourceStageRequestChoice(Enum):   # A subclass of Enum
    IDLE = 'Idle'
    DEVELOPMENT = 'Development'
    SANDBOXRequest = 'SandboxRequest'
    EMULATIONRequest = 'EmulationRequest'
    TESTBEDRequest = 'TestbedRequest'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ReservationStatusChoice(Enum):   # A subclass of Enum
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
        AerpawUser, related_name='experiment_of_experimenter'
    )
    project = models.ForeignKey(
        Project, related_name='experiment_of_project',null=True, on_delete=models.SET_NULL
    )
    created_by = models.ForeignKey(
        AerpawUser, related_name='experiment_created_by', null=True, on_delete=models.SET_NULL
    )
    created_date = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey(
        AerpawUser, related_name='experiment_modified_by', null=True, on_delete=models.SET_NULL
    )
    modified_date = models.DateTimeField(blank=True, null=True)
    #reservations = models.ForeignKey(
    #    'reservations.Reservation', related_name='experiment_of_reservation', null=True, on_delete=models.SET_NULL
    #)
    stage=models.CharField(
      max_length=64,
      choices=StageChoice.choices(),
    )
    profile = models.ForeignKey(
        Profile, related_name='experiment_profile',blank=True, null=True, on_delete=models.SET_NULL
    )
    key_inserted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'AERPAW Experiment'

    def __str__(self):
        return self.name

