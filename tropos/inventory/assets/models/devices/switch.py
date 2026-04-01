from django.db import models
from django.core.exceptions import ValidationError
from .device import Device

class Switch(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE, primary_key=True, related_name='switch')

    @property
    def fans(self):
        return self.device.fan_units.all()

    class Meta:
        db_table = "assets_switch"

    def __str__(self):
        return self.device.name
    
    def clean(self):
        if self.device.type != 'switch':
            raise ValidationError("Device type must me switch for switch instance")