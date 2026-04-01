# assets/models/device.py
from django.db import models
from django.utils import timezone
from inventory.common.custom_models import TimestampedModel

class NonDecommissionedQuerySet(models.QuerySet):
    def visible(self):
        # Exclude only decommissioned devices
        return self.exclude(status="decommissioned")
    
class Type(models.TextChoices):
    SERVER = 'server', 'Server'
    SWITCH = 'switch', 'Switch'
    APPLIANCE = 'appliance', 'Appliance'


class DeviceStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    DECOMMISSIONED = "decommissioned", "Decommissioned"


class Device(TimestampedModel):
    rack = models.ForeignKey('infrastructure.Rack', null=True,on_delete=models.PROTECT)
    rack_unit_allocations = models.PositiveSmallIntegerField(null=True)
    starting_position = models.PositiveSmallIntegerField(null=True)

    name = models.CharField(max_length=50, db_index=True, null=True)
    type = models.CharField(max_length=20,choices=Type.choices)
    model = models.CharField(max_length=50, null=True)
    serial_number = models.CharField(max_length=30, unique=True, null=True, db_index=True)
    ipv4_address = models.CharField(max_length=15, null=True)
    weight = models.PositiveIntegerField(null=True, blank=True)
    power = models.FloatField(null=True, blank=True)         # in Watts
    status = models.CharField(max_length=30, choices=DeviceStatus.choices,default=DeviceStatus.ACTIVE,db_index=True)   # optimize filtering by status)
    interface_count = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=300, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()  # default manager returns all
    non_decommissioned = NonDecommissionedQuerySet.as_manager()  # only devices that can use visible()

    def save(self, *args, **kwargs):
        """
        Always recompute status before saving.
        Status is system-controlled and should not be set manually.
        Rules:
        - If deleted_at is set → Decommissioned
        - Else if assigned to a rack → Active
        - Else → Inactive
        """
        if self.deleted_at:
            self.status = DeviceStatus.DECOMMISSIONED
        elif self.rack:
            self.status = DeviceStatus.ACTIVE
        else:
            self.status = DeviceStatus.INACTIVE

        super().save(*args, **kwargs)

    def soft_delete(self):
        """
        Soft delete a device by marking deleted_at
        and forcing status = Decommissioned.
        """
        self.deleted_at = timezone.now()
        self.save()
