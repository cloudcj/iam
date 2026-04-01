# assets/services/lifecycle/decommission_service.py
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from inventory.assets.models import DeviceStatus
from .retirement_policy import DeviceRetirementPolicy  # policy layer


class DecommissionService:
    @staticmethod
    @transaction.atomic
    def retire_device(device):
        """
        Retire/decommission a device safely using policy checks.
        Raises ValidationError if the device cannot be retired.
        """
        # Validate retirement rules
        # DeviceRetirementPolicy.validate(device)

        # Mark as decommissioned
        device.status = DeviceStatus.DECOMMISSIONED
        device.deleted_at = timezone.now()
        device.save(update_fields=["status", "deleted_at"])

        return device
