from django.db import models
from inventory.common.custom_models import TimestampedModel
from .floor import Floor
from .building import Building

class Room(TimestampedModel):
  number = models.CharField(max_length=30)
  floor = models.ForeignKey(Floor, on_delete=models.PROTECT)
  # building = models.ForeignKey(Building, on_delete=models.CASCADE,null=True,blank=True)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['number', 'floor'],
        name='unique_room_per_floor'
      )
    ]

  def __str__(self):
    return f"Room #{self.number}, Floor {self.floor.number}"