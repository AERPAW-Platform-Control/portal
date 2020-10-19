from django.db import models
from django.utils import timezone

from resources.models import Resources

# Create your models here.
class Reservation(models.Model):
    #_id = models.CharField(max_length=64)
    name=models.CharField(max_length=32)

    resource = models.ForeignKey(
        Resources, related_name='resource', on_delete=models.CASCADE
    )
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    virtualization=models.CharField(max_length=32)
    management_ip=models.GenericIPAddressField()
    state=models.CharField(max_length=32)

    def __str__(self):
        return self.name