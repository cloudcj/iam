# from django.db import models
# from .server import Device
# from inventory.enums.models.storage_type import StorageType

# class Type(models.TextChoices):
#   TB = 'tb', 'TB'
#   GB = 'gb', 'GB'

# class StorageUnit(models.Model):
#     device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="storage_units")
#     storage_type = models.ForeignKey(StorageType, on_delete=models.CASCADE, related_name="storage_units", default=1) # e.g., "HDD", "SSD", "NVMe"

#     storage_capacity = models.PositiveIntegerField()  # in GB
#     storage_count = models.PositiveIntegerField(default=0)  # how many drives
#     storage_unit = models.CharField(max_length=10, choices=Type.choices)   # e.g., "GB", "TB",

#     def __str__(self):
#         return f"{self.storage_count}x {self.storage_capacity}GB {self.storage_type}"
    
#     class Meta:
#         db_table = "assets_storage_unit"
    
from django.db import models
from django.core.exceptions import ValidationError

from ..devices.server import Device
from inventory.enums.models import StorageType,StorageFormFactor,StorageInterface,CapacityUnit

# Main storage unit model
class StorageUnit(models.Model):
    device = models.ForeignKey( Device,on_delete=models.CASCADE,related_name="storage_units")
    storage_type = models.CharField(max_length=10,choices=StorageType.choices,)
    storage_interface = models.ForeignKey(StorageInterface,on_delete=models.PROTECT,related_name="storage_units", null=True)
    form_factor = models.ForeignKey(StorageFormFactor,on_delete=models.PROTECT,related_name="storage_units", null=True)
    storage_capacity = models.PositiveIntegerField()  # numeric capacity
    storage_count = models.PositiveIntegerField(default=1)  # number of drives
    capacity_unit = models.CharField(max_length=10,choices=CapacityUnit.choices,default=CapacityUnit.GB)

    def __str__(self):
        return (
            f"{self.storage_count}x {self.storage_capacity}{self.capacity_unit} "
            f"{self.storage_type} ({self.storage_interface.name}, {self.form_factor.name})"
        )

    class Meta:
        db_table = "assets_storage_unit"

    def clean(self):
    
        if self.device.device_type not in ["server", "appliance","analyzer"]:
            raise ValidationError("Only servers and appliances may have processor units.")
    
