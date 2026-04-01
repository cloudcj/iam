from django.db import models
from inventory.common.custom_models import TimestampedModel
from .building import Building

class Floor(TimestampedModel):
  number = models.PositiveSmallIntegerField()
  building = models.ForeignKey(Building, on_delete=models.PROTECT)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['number', 'building'],
        name='unique_floor_per_building'
      )
    ]

  def __str__(self):
    return f"Floor {self.number}, Building {self.building.name}"