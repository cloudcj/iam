# assets/services/device/appliance_service.py
from django.db import transaction
from inventory.assets.models import (
    Appliance,
    Device,
    Type,
    MemoryUnit,
    ProcessorUnit,
    StorageUnit,
    PowerSupplyUnit,
)
from .base_device_service import BaseDeviceService


class ApplianceService(BaseDeviceService):

    @staticmethod
    def _sync_units(device, nested_data):
        """
        Sync appliance compute and power units.
        """
        unit_map = {
            "memory_units": MemoryUnit,
            "processor_units": ProcessorUnit,
            "storage_units": StorageUnit,
            "power_supply_units": PowerSupplyUnit,
        }

        for key, model in unit_map.items():
            items = nested_data.get(key)
            if items is None:
                continue

            existing = {u.id: u for u in getattr(device, key).all()}
            new_ids = set()

            for item in items:
                uid = item.get("id")
                if uid and uid in existing:
                    unit = existing[uid]
                    for attr, val in item.items():
                        if attr != "id":
                            setattr(unit, attr, val)
                    unit.save()
                    new_ids.add(uid)
                else:
                    model.objects.create(device=device, **item)

            stale_ids = [u.id for u in existing.values() if u.id not in new_ids]
            if stale_ids:
                model.objects.filter(id__in=stale_ids).delete()

    # -------------------------------------------------

    @staticmethod
    @transaction.atomic
    def provision_appliance(device_data, appliance_data, nested_data):
        """
        Create appliance + device + rack + units + interfaces.
        """
        device = BaseDeviceService.provision_device(
            device_type=Type.APPLIANCE,
            device_data=device_data,
            nested_data=nested_data,
        )

        appliance = Appliance.objects.create(device=device, **appliance_data)

        ApplianceService._sync_units(device, nested_data)
        BaseDeviceService._handle_interfaces(device, nested_data, is_create=True)

        return appliance

    # -------------------------------------------------

    @staticmethod
    @transaction.atomic
    def reconfigure_appliance(instance, device_data=None, appliance_data=None, nested_data=None):
        """
        Update appliance + device + rack + units + interfaces.
        """
        device_data = device_data or {}
        appliance_data = appliance_data or {}
        nested_data = nested_data or {}

        BaseDeviceService.reconfigure_device(
            instance.device,
            device_data=device_data,
            nested_data=nested_data,
        )

        for attr, val in appliance_data.items():
            setattr(instance, attr, val)
        instance.save()

        ApplianceService._sync_units(instance.device, nested_data)
        BaseDeviceService._handle_interfaces(instance.device, nested_data, is_create=False)

        return instance

    # -------------------------------------------------

    @staticmethod
    @transaction.atomic
    def retire_appliance(appliance: Appliance):
        """
        Standardized appliance retirement.
        """
        return BaseDeviceService.retire_device(appliance.device)
