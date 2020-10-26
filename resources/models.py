from django.db import models
from django.contrib.auth import get_user_model
from enum import Enum

from projects.models import Project
from accounts.models import AerpawUser

User = get_user_model()

class ResourceStageChoice(Enum):   # A subclass of Enum
    IDEL = 'Idel'
    DEVELOPMENT = 'Development'
    SANDBOX = 'Sandbox'
    EMULATION = 'Emulation'
    TESTBED = 'Testbed'

class ResourceTypeChoice(Enum):   # A subclass of Enum
    CLOUD= 'Cloud'
    SANDBOX = 'Sandbox'
    FIXEDNODE = 'FixedNode'
    PORTABLENODE = 'PortableNode'
    OTHERS = 'Others'

class ResourceLocationChoice(Enum):   # A subclass of Enum
    DCS = 'DCS'
    LAKEWHEELER = 'LakeWheeler'
    CENTENNIAL = 'Centennial'
    CARY = 'Cary'
    OTHERS = 'Others'

# Create your models here.
class Resource(models.Model):
    admin=models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    name=models.CharField(max_length=32)
    description = models.TextField()
    resourceType=models.CharField(
      max_length=5,
      choices=[(tag, tag.value) for tag in ResourceTypeChoice]  # Choices is a list of Tuple
    )

    units=models.PositiveSmallIntegerField(default=1)
    availableUnits=models.PositiveSmallIntegerField(default=1)
    location=models.CharField(max_length=32)
    
    stage=models.CharField(
      max_length=5,
      choices=[(tag, tag.value) for tag in ResourceStageChoice]  # Choices is a list of Tuple
    )

    def has_inventory(self):
        return self.units > 0

    
