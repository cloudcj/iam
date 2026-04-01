# assets/services/lifecycle/retirement_policy.py
from django.core.exceptions import ValidationError

class DeviceRetirementPolicy:

    @staticmethod
    def validate(device):
        """
        Raises ValidationError if the device cannot be retired.
        """

        # Example: device is already decommissioned
        if device.status == "DECOMMISSIONED":
            raise ValidationError("Device is already decommissioned.")

        # Example: device still has active interfaces
        if device.interfaces.filter(is_connected=True).exists():
            raise ValidationError("Cannot retire device with active interfaces.")

        # Example: device still occupies a rack
        if device.rack is not None:
            raise ValidationError("Cannot retire device still assigned to a rack.")

        # You can add more rules here (environment, VMs, etc.)
