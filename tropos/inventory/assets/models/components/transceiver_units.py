from django.db import models
from inventory.common.custom_models import TimestampedModel
from .interface import Interface
from inventory.enums.models.transceiver_type_enums import TransceiverType

class TransceiverUnit(TimestampedModel):
    """
    Represents a transceiver module installed on a specific interface.
    """
    interface = models.ForeignKey(
        Interface,
        on_delete=models.CASCADE,
        related_name='transceiver_units'
    )
    transceiver_type = models.ForeignKey(
        TransceiverType,
        on_delete=models.PROTECT,
        related_name='transceiver_units'
    )

    class Meta:
        db_table = "assets_transceiver_unit"
        verbose_name = "Transceiver Unit"
        verbose_name_plural = "Transceiver Units"

    def __str__(self):
        return f"{self.transceiver_type.name} on Interface {self.interface.id}"
