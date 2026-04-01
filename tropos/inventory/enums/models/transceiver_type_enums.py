from django.db import models
from inventory.common.custom_models import TimestampedModel

class TransceiverType(TimestampedModel):
    """
    Stores the types of transceivers (e.g., SFP, QSFP, SFP+, QSFP28).
    """
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "enums_transceiver_type"
        verbose_name = "Transceiver Type"
        verbose_name_plural = "Transceiver Types"

    def __str__(self):
        return self.name
