from django.db import models
from inventory.common.custom_models import TimestampedModel

class Region(TimestampedModel):
  name = models.CharField(max_length=25, unique=True)

  def __str__(self):
    return self.name