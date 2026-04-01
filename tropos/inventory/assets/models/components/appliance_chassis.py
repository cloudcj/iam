# assets/models/appliance_chassis.py
from django.db import models
from ..devices import Device

class ApplianceChassis(models.Model):
    """
    Represents a module or slot inside a chassis-type appliance (e.g., Firewall, Anti-DDoS).
    Each chassis is attached to a Device record for interface and port mapping.
    """
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name="chasis_modules"
    )
    module_name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    slot_position = models.PositiveIntegerField()
    is_occupied = models.BooleanField(default=False)
    is_chassis = models.BooleanField(default=False)


    class Meta:
        db_table = "assets_appliance_chassis"
        verbose_name = "Appliance Chasis Module"
        verbose_name_plural = "Appliance Chasis Modules"
        unique_together = ("device", "slot_position")


    def __str__(self):
        return f"{self.module_name} ({self.serial_number}) in Slot {self.slot_position}"
