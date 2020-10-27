from django.db import models
from django.utils import timezone
import uuid

from resources.models import Resource
from experiments.models import Experiment, ReservationStateChoice

# Create your models here.
class Reservation(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=32)
    description = models.TextField()

    experiment = models.ForeignKey(
        Experiment, related_name='reservation_experiment', on_delete=models.CASCADE
    )

    resource = models.ForeignKey(
        Resource, related_name='reservation_resource', on_delete=models.CASCADE
    )
    units = models.IntegerField()
    
    start_date = models.DateTimeField(default=timezone.now) #should come frome experiment time
    end_date = models.DateTimeField(default=timezone.now)
    virtualization=models.CharField(max_length=32)
    management_ip=models.GenericIPAddressField()

    state=models.CharField(
      max_length=64,
      choices=ReservationStateChoice.choices(),
    )

    def __str__(self):
        return self.name
