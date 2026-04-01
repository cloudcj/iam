# assets/models/interface.py
from django.db import models
from inventory.common.custom_models import TimestampedModel
from ..devices import Device

class Interface(TimestampedModel):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='interfaces'  # important for nested serializers
    )
    interface_number = models.PositiveSmallIntegerField()
    to_location = models.CharField(max_length=100, null=True, blank=True)
    cable_type = models.CharField(max_length=100, null=True, blank=True)
    port_type = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['device', 'interface_number'],
                name='uniq_device_interface_number'
            )
        ]
        ordering = ['interface_number']  # optional: always order by number

    def __str__(self):
        return f"{self.device} - Interface {self.interface_number}"
