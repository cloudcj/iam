from django.db import models
from django.core.exceptions import ValidationError
from .device import Device

class Server(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE, primary_key=True)
    classification = models.CharField(max_length=100)
    module_name = models.CharField(max_length=100)

    @property
    def fans(self):
        return self.device.fan_units.all()

    class Meta:
        db_table = "assets_server"

    def __str__(self):
        return self.device.name
    
    def clean(self):
        if self.device.type != 'server':
            raise ValidationError("Device type must me switch for switch instance")
