# assets/services/device/base_device_service.py
from django.db import transaction
from inventory.assets.models import Device, Type
from ...services.rack.rack_service import RackService
from inventory.assets.services.interface.interface_service import InterfaceService
from inventory.assets.services.lifecycle.decommision_service import DecommissionService


class BaseDeviceService:

    @staticmethod
    def _handle_interfaces(device, nested_data, is_create=True):
        """
        Sync interfaces using InterfaceService and update interface_count on the device.
        """
        count = nested_data.get("interface_count")
        if count is None:
            return

        if is_create:
            InterfaceService.create_interfaces(device, count)
        else:
            InterfaceService.sync_interfaces(device, count)

        device.interface_count = int(count)
        device.save(update_fields=["interface_count"])

    @staticmethod
    def _validate_and_allocate_rack(device, rack, start, alloc):
        """
        Validate and allocate rack positions if positions have changed.
        """
        positions_changed = (
            rack != device.rack or
            start != device.starting_position or
            alloc != device.rack_unit_allocations
        )

        if positions_changed:
            RackService.validate_positions(rack, start, alloc, exclude_device=device)
            RackService.release_device_from_positions(
                device.rack, device.starting_position, device.rack_unit_allocations, device
            )
            device.rack = rack
            device.starting_position = start
            device.rack_unit_allocations = alloc
            device.save(update_fields=["rack", "starting_position", "rack_unit_allocations"])
            RackService.assign_device_to_positions(rack, start, alloc, device)

    @staticmethod
    @transaction.atomic
    def retire_device(device):
        """
        Standardized retirement using policy + decommission service.
        """
        return DecommissionService.retire_device(device)

    @staticmethod
    @transaction.atomic

    def provision_device(device_type, device_data, nested_data):
        """
        Create a Device instance and optionally allocate rack and interfaces.
        Validates rack positions before creating the device to prevent conflicts.
        """
        # Extract fields
        rack = device_data.get("rack")
        start = device_data.get("starting_position")
        alloc = device_data.get("rack_unit_allocations")
        interface_count = nested_data.get("interface_count", 0)

        # ✅ Validate rack BEFORE creating device
        if rack and start and alloc:
            RackService.validate_positions(rack, start, alloc)

        # Create device
        device = Device.objects.create(
            type=device_type,
            rack=rack,
            name=device_data.get("name"),
            model=device_data.get("model"),
            serial_number=device_data.get("serial_number"),
            ipv4_address=device_data.get("ipv4_address"),
            rack_unit_allocations=alloc,
            starting_position=start,
            interface_count=interface_count,
            weight=device_data.get("weight"),
            power=device_data.get("power"),
            description=device_data.get("description"),
        )

        # Allocate rack positions
        if rack and start and alloc:
            RackService.assign_device_to_positions(rack, start, alloc, device)

        # Handle interfaces
        if interface_count:
            InterfaceService.create_interfaces(device, interface_count)

        return device

    # def provision_device(device_type, device_data, nested_data):
    #     """
    #     Create a Device instance and optionally allocate rack and interfaces.
    #     """
    #     # Extract fields from device_data
    #     rack = device_data.get("rack")
    #     start = device_data.get("starting_position")
    #     alloc = device_data.get("rack_unit_allocations")
    #     interface_count = nested_data.get("interface_count")

    #     # Create the device
    #     device = Device.objects.create(
    #         type=device_type,
    #         rack=rack,
    #         name=device_data.get("name"),
    #         model=device_data.get("model"),
    #         serial_number=device_data.get("serial_number"),
    #         ipv4_address=device_data.get("ipv4_address"),
    #         rack_unit_allocations=alloc,
    #         starting_position=start,
    #         interface_count=interface_count or 0,
    #         weight=device_data.get("weight"),
    #         power=device_data.get("power"),
    #         description=device_data.get("description"),
    #     )

    #     # Allocate rack positions if provided
    #     if rack and start and alloc:
    #         BaseDeviceService._validate_and_allocate_rack(device, rack, start, alloc)

    #     # Handle interfaces
    #     BaseDeviceService._handle_interfaces(device, nested_data, is_create=True)

    #     return device

    @staticmethod
    @transaction.atomic
    def reconfigure_device(device, device_data=None, nested_data=None, extra_fields=None):
        """
        Update an existing Device instance:
        - update common fields from device_data
        - apply extra device-specific fields
        - re-allocate rack positions if changed
        - update interfaces
        """
        device_data = device_data or {}
        nested_data = nested_data or {}
        extra_fields = extra_fields or {}

        fields_to_update = []

        # Update common fields
        for field in ["name","model","serial_number", "ipv4_address", "weight", "power", "description"]:
            if field in device_data:
                setattr(device, field, device_data[field])
                fields_to_update.append(field)

        # Update extra device-specific fields
        for field, value in extra_fields.items():
            setattr(device, field, value)
            fields_to_update.append(field)

        # Validate and allocate rack if changed
        rack = device_data.get("rack", device.rack)
        start = device_data.get("starting_position", device.starting_position)
        alloc = device_data.get("rack_unit_allocations", device.rack_unit_allocations)
        if rack and start and alloc:
            BaseDeviceService._validate_and_allocate_rack(device, rack, start, alloc)

        # Update interface count if provided
        interface_count = nested_data.get("interface_count")
        if interface_count is not None:
            device.interface_count = interface_count
            fields_to_update.append("interface_count")

        # Save updated fields
        if fields_to_update:
            device.save(update_fields=fields_to_update)

        # Sync interfaces
        BaseDeviceService._handle_interfaces(device, nested_data, is_create=False)

        return device
