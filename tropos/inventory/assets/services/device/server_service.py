# assets/services/device/server_service.py
from django.db import transaction
from inventory.assets.models import Server, Device, Type, MemoryUnit, ProcessorUnit, StorageUnit, PowerSupplyUnit, FanUnit
from .base_device_service import BaseDeviceService
from ..rack.rack_service import RackService


class ServerService(BaseDeviceService):

    @staticmethod
    def _sync_units(device, nested_data):
        """
        Update or create server-specific nested units: memory, CPU, storage, PSU, Fan.
        """
        unit_map = {
            "memory_units": MemoryUnit,
            "processor_units": ProcessorUnit,
            "storage_units": StorageUnit,
            "power_supply_units": PowerSupplyUnit,
        }

        for key, model in unit_map.items():
            items = nested_data.get(key)
            if not items:
                continue

            existing = {u.id: u for u in getattr(device, key).all()}
            new_ids = set()

            for item in items:
                uid = item.get("id")
                if uid and uid in existing:
                    unit = existing[uid]
                    # for attr, val in item.items():
                    #     setattr(unit, attr, val)
                    for attr, val in item.items():
                        if attr != "id":
                            setattr(unit, attr, val)
                    unit.save()
                    new_ids.add(uid)
                else:
                    model.objects.create(device=device, **item)

            # Delete units not in payload
            to_delete = [u.id for u in existing.values() if u.id not in new_ids]
            if to_delete:
                model.objects.filter(id__in=to_delete).delete()

        # Fan units (special handling)
        fans = nested_data.get("fan_units")
        if fans:
            existing = {f.id: f for f in device.fan_units.all()}
            new_ids = set()
            for i, unit in enumerate(fans):
                uid = unit.get("id")
                if uid and uid in existing:
                    fan = existing[uid]
                    for attr, val in unit.items():
                        setattr(fan, attr, val)
                    fan.save()
                    new_ids.add(uid)
                else:
                    FanUnit.objects.create(
                        device=device,
                        fan_count=unit.get("fan_count", 1),
                        fan_speed=unit.get("fan_speed", 0),
                        is_internal=unit.get("is_internal", True),
                        wattage_max_output=unit.get("wattage_max_output", 0.0),
                        wattage_average=unit.get("wattage_average", 0.0),
                        description=unit.get("description", f"Auto-generated fan {i+1}"),
                        psu_id=unit.get("psu"),
                    )
            to_delete = [f.id for f in existing.values() if f.id not in new_ids]
            if to_delete:
                FanUnit.objects.filter(id__in=to_delete).delete()

    @staticmethod
    @transaction.atomic
    def provision_server(device_data, server_data, nested_data):
        """
        Create server + device + nested units + rack allocation + interfaces.
        """
        # Create device (handles rack & interfaces)
        device = BaseDeviceService.provision_device(
            device_type=Type.SERVER,
            device_data=device_data,
            nested_data=nested_data,
        )

        # Create server
        server = Server.objects.create(device=device, **server_data)

        # Sync server-specific units
        ServerService._sync_units(device, nested_data)

        return server


    
    # def provision_server(device_data, server_data, nested_data):
    #     """
    #     Create server + device + nested units + rack allocation + interfaces.
    #     """
    #     rack = device_data.get("rack")
    #     start = device_data.get("starting_position")
    #     alloc = device_data.get("rack_unit_allocations")
    #     interface_count = nested_data.get("interface_count", 0)

    #     # Validate rack
    #     RackService.validate_positions(rack, start, alloc)

    #     # Create device
    #     device = BaseDeviceService.provision_device(
    #         device_type=Type.SERVER,
    #         device_data=device_data,
    #         nested_data=nested_data,
    #     )

    #     # Allocate rack
    #     RackService.assign_device_to_positions(rack, start, alloc, device)

    #     # Create server
    #     server = Server.objects.create(device=device, **server_data)

    #     # Sync units and interfaces
    #     ServerService._sync_units(device, nested_data)
    #     ServerService._handle_interfaces(device, nested_data, is_create=True)

    #     return server

    @staticmethod
    @transaction.atomic


    def reconfigure_server(instance, device_data=None, server_data=None, nested_data=None):
        """
        Update server + device + nested units + interfaces.
        """
        device = instance.device
        device_data = device_data or {}
        server_data = server_data or {}
        nested_data = nested_data or {}

        # Update device + interfaces + rack
        BaseDeviceService.reconfigure_device(
            device,
            device_data=device_data,
            nested_data=nested_data,
        )

        # Update server-specific fields
        for attr, val in server_data.items():
            setattr(instance, attr, val)
        instance.save()

        # Sync server-specific units
        ServerService._sync_units(device, nested_data)

        return instance

    
    # def reconfigure_server(instance, device_data=None, server_data=None, nested_data=None):
    #     """
    #     Update server + device + nested units + interfaces.
    #     """
    #     device = instance.device
    #     device_data = device_data or {}
    #     server_data = server_data or {}
    #     nested_data = nested_data or {}


    #     # Rack allocation
    #     new_rack = device_data.get("rack", device.rack)
    #     new_start = device_data.get("starting_position", device.starting_position)
    #     new_alloc = device_data.get("rack_unit_allocations", device.rack_unit_allocations)
    #     BaseDeviceService._validate_and_allocate_rack(device, new_rack, new_start, new_alloc)

    #     BaseDeviceService.reconfigure_device(
    #         instance.device,
    #         device_data=device_data,
    #         nested_data=nested_data,
    #     )

    #     # Server fields
    #     for attr, val in server_data.items():
    #         setattr(instance, attr, val)
    #     instance.save()

    #     # Nested units + interfaces
    #     ServerService._sync_units(device, nested_data)
    #     BaseDeviceService._handle_interfaces(device, nested_data, is_create=False)

    #     return instance

    @staticmethod
    @transaction.atomic
    def retire_server(server: Server):
        """
        Standardized retirement of a server.
        """
        return BaseDeviceService.retire_device(server.device)
