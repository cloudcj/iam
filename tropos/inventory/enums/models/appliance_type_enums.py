from django.db import models
from inventory.common.custom_models import TimestampedModel

class ApplianceType(models.Model):
    name = models.CharField(max_length=100)
    is_chassis = models.BooleanField(default=False)
    has_compute_units = models.BooleanField(default=False)

    class Meta:
        db_table = "enums_appliance_type"

    def __str__(self):
        return self.name

