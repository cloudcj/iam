from django.db import models
from inventory.common.custom_models import TimestampedModel
from .availability_zone import AvailabilityZone

class Building(TimestampedModel):
  name = models.CharField(max_length=25, unique=True)
  availability_zone = models.ForeignKey(AvailabilityZone, on_delete=models.PROTECT, null=True)

  def __str__(self):
    return f"Building {self.name}, {self.availability_zone.location}"