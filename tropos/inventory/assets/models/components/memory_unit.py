from django.db import models
from ..devices.server import Device
from django.core.exceptions import ValidationError

class MemoryUnit(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="memory_units")
    ram_capacity = models.PositiveIntegerField()  # e.g., in GB
    quantity = models.PositiveIntegerField(null=True)
    # brand_description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ram_capacity}GB - {self.brand_description}"
    
    class Meta:
            db_table = "assets_memory_unit"


    # Validation (can only be assigned to server and appliance)

    def clean(self):
        if self.device.device_type not in ["server", "appliance"]:
            raise ValidationError("Only servers and appliances may have memory units.")