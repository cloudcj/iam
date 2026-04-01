from django.db import models
from inventory.common.custom_models import TimestampedModel
from ..devices import Device

class PowerSupplyUnit(TimestampedModel):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="power_supply_units")
    heat_dissipation = models.FloatField(default=0)
    max_output = models.PositiveSmallIntegerField()
    average_output = models.FloatField(null=True, blank=True)
    wattage_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    power_type = models.CharField(max_length=100, default="")
    connector_type = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=300, null=True)

    @property
    def fans(self):
        return self.device.fan_units.all()

    class Meta:
        db_table = "assets_power_supply_unit"

    def __str__(self):
        return f"PSU {self.power_type}"
