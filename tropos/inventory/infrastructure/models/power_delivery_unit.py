from django.db import models
from inventory.common.custom_models import TimestampedModel
from .rack import Rack

class Type(models.TextChoices):
  LEFT = "left", "Left"
  RIGHT = "right", "Right"

class PowerDeliveryUnit(TimestampedModel):
  rack = models.ForeignKey(
    Rack,
    on_delete=models.CASCADE,
    related_name="power_delivery_units",
  )
  position = models.CharField(max_length=10, choices=Type.choices)
  max_output = models.PositiveIntegerField(blank=True, default=0)
  description = models.CharField(max_length=300, null=True, blank=True)

  class Meta:
    db_table = "infrastructure_power_delivery_units"
    constraints = [
      models.UniqueConstraint(
        fields=["position", "rack"],
          name="unique_pdu_position_per_rack"
      )
    ]

  def __str__(self):
    return f"Postion {self.position}, Rack {self.rack.number}"

class PowerDeliveryUnitOutlet(TimestampedModel):
  power_delivery_unit = models.ForeignKey(
    PowerDeliveryUnit,
    on_delete=models.CASCADE,
    related_name="power_delivery_unit",
    )

  outlet_number = models.PositiveSmallIntegerField()
  to_location = models.CharField(max_length=100, null=True)
  description = models.CharField(max_length=300, null=True)

  class Meta:
    db_table = "infrastructure_power_delivery_unit_outlet"
    constraints = [
      models.UniqueConstraint(
        fields=['outlet_number', 'power_delivery_unit'],
        name='unique_outlet_number_per_pdu'
      )
    ]