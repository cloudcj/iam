from django.db import models
from inventory.common.custom_models import TimestampedModel
from ..devices import Device

class FanUnit(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="fan_units")
    psu = models.ForeignKey(
        "PowerSupplyUnit", 
        on_delete=models.CASCADE, 
        related_name="fan_units", 
        null=True, 
        blank=True
    )
    fan_count = models.IntegerField(default=1)
    fan_speed = models.IntegerField(default=0, null=True)
    is_internal = models.BooleanField(default=True, null=True)
    wattage_max_output = models.FloatField(default=0.0, null=True)
    wattage_average = models.FloatField(default=0.0, null=True)
    description = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "assets_fan_unit"
