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

    def __str__(self):
        return self.name

    def has_inventory(self):
        return self.units > 0

    
