from django.db import models
from inventory.common.custom_models import TimestampedModel
from .device import Device
from inventory.enums.models.appliance_type_enums import ApplianceType


class Appliance(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE, primary_key=True)
    appliance_type = models.ForeignKey(ApplianceType, on_delete=models.PROTECT, null=True)

    # appliance_name = models.CharField(max_length=200, null=True)
    is_chassis = models.BooleanField(default=False)
    has_components_units = models.BooleanField(default=False)

    class Meta:
        db_table = "assets_appliance"
        verbose_name = "Appliance"
        verbose_name_plural = "Appliances"

    def __str__(self):
        return self.device.name or f"{self.appliance_type.name} Appliance ({self.device.serial_number})"

    @property
    def fans(self):
        return self.device.fan_units.all()

    @property
    def interfaces(self):
        return self.device.interfaces.all()