from django.db import models
from inventory.common.custom_models import TimestampedModel
from .room import Room

class Pod(TimestampedModel):
  name = models.CharField(max_length=100)
  room = models.ForeignKey(Room, on_delete=models.PROTECT)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['name', 'room'],
        name='unique_pod_per_room'
      )
    ]
  
  def __str__(self):
    return self.name