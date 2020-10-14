from django.db import models

from projects.models import Project

# Create your models here.
class Inventory(models.Model):
    #_id = models.CharField(max_length=64)
    name=models.CharField(max_length=32)
    resourceType=models.PositiveSmallIntegerField(default=0)
    units=models.PositiveSmallIntegerField(default=0)
    availableUnits=models.PositiveSmallIntegerField(default=0)
    location=models.CharField(max_length=32)
    stage=models.CharField(max_length=32)

