from django.db import models
from inventory.common.custom_models import TimestampedModel
from .region import Region


class AvailabilityZone(TimestampedModel):
  name = models.CharField(max_length=25, unique=True )
  location = models.CharField(max_length=100)
  region = models.ForeignKey(Region, on_delete=models.PROTECT)

  class Meta:
        db_table = "infrastructure_availability_zone"

  def __str__(self):
        return f"{self.name} ({self.location})"
