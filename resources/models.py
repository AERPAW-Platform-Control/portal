from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from enum import Enum
import uuid

from accounts.models import AerpawUser

User = get_user_model()

class ResourceStageChoice(Enum):   # A subclass of Enum
    IDLE = 'Idle'
    DEVELOPMENT = 'Development'
    SANDBOX = 'Sandbox'
    EMULATION = 'Emulation'
    TESTBED = 'Testbed'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class ResourceTypeChoice(Enum):   # A subclass of Enum
    CLOUD= 'Cloud'
    SANDBOX = 'Sandbox'
    FIXEDNODE = 'FixedNode'
    PORTABLENODE = 'PortableNode'
    OTHERS = 'Others'
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class ResourceLocationChoice(Enum):   # A subclass of Enum
    DCS = 'DCS'
    LAKEWHEELER = 'LakeWheeler'
    CENTENNIAL = 'Centennial'
    CARY = 'Cary'
    OTHERS = 'Others'
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

# Create your models here.
class Resource(models.Model):
    admin=models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)

    name=models.CharField(max_length=32)
    description = models.TextField()
    resourceType=models.CharField(
      max_length=64,
      choices=ResourceTypeChoice.choices(),
    )

    units=models.PositiveSmallIntegerField(default=1)
    availableUnits=models.PositiveSmallIntegerField(default=1)
    location=models.CharField(
      max_length=64,
      choices=ResourceLocationChoice.choices(),
    )
    
    stage=models.CharField(
      max_length=64,
      choices=ResourceStageChoice.choices(),
    )

    created_date=models.DateTimeField(default=timezone.now)

    @property
    def reservation_btn_title(self):
      if self.is_available():
        return "Reserve"
      else:
        return "Can not reserve"


    def __str__(self):
      return self.name

    def is_units_available(self):
      return (self.units > 0) 

    def is_units_available_reservation(self, count):
      return (self.units - count > 0) 

    def is_correct_stage(self,stage):
      return (stage == self.stage) 

    def remove_units(self, count=1, save=True):
      current_availableUnits = self.availableUnits
      current_availableUnits -= count
      if current_availableUnits >= 0:
        self.availableUnits = current_availableUnits
        if save == True:
          self.save()
        return True
      return False

    def get_resource_stage(self):
      return self.stage
