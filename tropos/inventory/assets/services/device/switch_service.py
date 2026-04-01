# assets/services/device/switch_service.py
from django.db import transaction
from inventory.assets.models import Switch, Device, Type, FanUnit, PowerSupplyUnit
from .base_device_service import BaseDeviceService
from ..rack.rack_service import RackService


class SwitchService(BaseDeviceService):

    @staticmethod
    def _sync_units(device, nested_data):
        """
        Update or create switch-specific nested units: PSU and Fans.
        """
        unit_map = {
            "power_supply_units": PowerSupplyUnit,
        }

        # Sync PSUs
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
                    for attr, val in item.items():
                        setattr(unit, attr, val)
                    unit.save()
                    new_ids.add(uid)
                else:
                    model.objects.create(device=device, **item)

            # Delete units not in payload
            to_delete = [u.id for u in existing.values() if u.id not in new_ids]
            if to_delete:
                model.objects.filter(id__in=to_delete).delete()

        # # Sync FanUnits
        # fan_units = nested_data.get("fan_units")
        # if fan_units:
        #     existing = {f.id: f for f in device.fan_units.all()}
        #     new_ids = set()
        #     for i, unit in enumerate(fan_units):
        #         uid = unit.get("id")
        #         if uid and uid in existing:
        #             fan = existing[uid]
        #             for attr, val in unit.items():
        #                 setattr(fan, attr, val)
        #             fan.save()
        #             new_ids.add(uid)
        #         else:
        #             FanUnit.objects.create(
        #                 device=device,
        #                 fan_count=unit.get("fan_count", 1),
        #                 fan_speed=unit.get("fan_speed", 0),
        #                 is_internal=unit.get("is_internal", True),
        #                 wattage_max_output=unit.get("wattage_max_output", 0.0),
        #                 wattage_average=unit.get("wattage_average", 0.0),
        #                 description=unit.get("description", f"Auto-generated fan {i+1}"),
        #                 psu_id=unit.get("psu"),
        #             )

        #     # Delete fans not in payload
        #     to_delete = [f.id for f in existing.values() if f.id not in new_ids]
        #     if to_delete:
        #         FanUnit.objects.filter(id__in=to_delete).delete()

    @staticmethod
    @transaction.atomic

    
    
    def provision_switch(device_data, switch_data, nested_data):
        """
        Create a switch + device + nested units + rack allocation + interfaces.
        """

        rack = device_data.get("rack")
        start = device_data.get("starting_position")
        alloc = device_data.get("rack_unit_allocations")
        interface_count = nested_data.get("interface_count", 0)

        # Validate rack
        RackService.validate_positions(rack, start, alloc)

        device = BaseDeviceService.provision_device(
            device_type=Type.SWITCH,
            device_data=device_data,
            nested_data=nested_data,
        )

        # Allocate rack
        RackService.assign_device_to_positions(rack, start, alloc, device)

        # Create switch
        switch = Switch.objects.create(device=device, **switch_data)

        # Sync units and interfaces
        SwitchService._sync_units(device, nested_data)
        BaseDeviceService._handle_interfaces(device, nested_data, is_create=True)


        return switch

  
    @staticmethod
    @transaction.atomic
    def reconfigure_switch(instance, device_data=None, nested_data=None):
        """
        Update a switch (Device) along with nested units and interfaces.
        """
        device_data = device_data or {}
        nested_data = nested_data or {}

        # -----------------------
        # Rack allocation
        # -----------------------
        BaseDeviceService.reconfigure_device(
            instance.device,
            device_data=device_data,
            nested_data=nested_data
        )

        SwitchService._sync_units(instance.device, nested_data)
        BaseDeviceService._handle_interfaces(instance.device, nested_data, is_create=False)

        return instance



    # def reconfigure_switch(instance, device_data=None, switch_data=None, nested_data=None):
    #     """
    #     Update switch + device + nested units + interfaces.
    #     """
    #     device = instance  # your instance is a Device object
    #     device_data = device_data or {}
    #     switch_data = switch_data or {}
    #     nested_data = nested_data or {}

    #     # Rack allocation
    #     new_rack = device_data.get("rack", device.rack)
    #     new_start = device_data.get("starting_position", device.starting_position)
    #     new_alloc = device_data.get("rack_unit_allocations", device.rack_unit_allocations)
    #     BaseDeviceService._validate_and_allocate_rack(device, new_rack, new_start, new_alloc)

    #     # Update Device fields
    #     device_fields = ["name", "serial_number", "ipv4_address", "model", "weight", "power", "description", "interface_count"]
    #     for field in device_fields:
    #         if field in device_data:
    #             setattr(device, field, device_data[field])
    #     device.save()  # 🔑 save Device

    #     # Update Switch-specific fields (if any)
    #     for attr, val in switch_data.items():
    #         setattr(device.switch, attr, val)  # use related Switch instance
    #     device.switch.save()  # 🔑 save Switch

    #     # Nested units + interfaces
    #     SwitchService._sync_units(device, nested_data)
    #     BaseDeviceService._handle_interfaces(device, nested_data, is_create=False)

    #     return device

    @staticmethod
    @transaction.atomic
    def retire_switch(switch: Switch):
        """
        Standardized retirement of a switch.
        """
        return BaseDeviceService.retire_device(switch.device)













    # def provision_switch(device_data, switch_data, nested_data):
    #     """
    #     Create a switch + device + nested units + rack allocation + interfaces.
    #     """
    #     rack = device_data.get("rack")
    #     start = device_data.get("starting_position")
    #     alloc = device_data.get("rack_unit_allocations")
    #     interface_count = nested_data.get("interface_count", 0)

    #     # Validate rack
    #     RackService.validate_positions(rack, start, alloc)

    #     # Create device
    #     device = Device.objects.create(
    #         type=Type.SWITCH,
    #         rack=rack,
    #         name=device_data.get("name"),
    #         model=device_data.get("model"),
    #         serial_number=device_data.get("serial_number"),
    #         ipv4_address=device_data.get("ipv4_address"),
    #         rack_unit_allocations=alloc,
    #         starting_position=start,
    #         interface_count=interface_count,
    #         weight=device_data.get("weight"),
    #         power=device_data.get("power"),
    #         description=device_data.get("description"),
    #     )

    #     # Allocate rack
    #     RackService.assign_device_to_positions(rack, start, alloc, device)

    #     # Create switch
    #     switch = Switch.objects.create(device=device, **switch_data)

    #     # Sync units and interfaces
    #     SwitchService._sync_units(device, nested_data)
    #     BaseDeviceService._handle_interfaces(device, nested_data, is_create=True)

    #     return switch










    #  def reconfigure_appliance(instance, device_data=None, appliance_data=None, nested_data=None):
    #     """
    #     Update appliance + device + rack + units + interfaces.
    #     """
    #     device_data = device_data or {}
    #     appliance_data = appliance_data or {}
    #     nested_data = nested_data or {}

    #     BaseDeviceService.reconfigure_device(
    #         instance.device,
    #         device_data=device_data,
    #         nested_data=nested_data,
    #     )

    #     for attr, val in appliance_data.items():
    #         setattr(instance, attr, val)
    #     instance.save()

    #     ApplianceService._sync_units(instance.device, nested_data)
    #     BaseDeviceService._handle_interfaces(instance.device, nested_data, is_create=False)

    #     return instance

    
    
    # def reconfigure_switch(instance, device_data=None, nested_data=None):
    #     """
    #     Update a switch (Device) along with nested units and interfaces.
    #     """
    #     device_data = device_data or {}
    #     nested_data = nested_data or {}

    #     # -----------------------
    #     # Rack allocation
    #     # -----------------------
    #     new_rack = device_data.get("rack", device.rack)
    #     new_start = device_data.get("starting_position", device.starting_position)
    #     new_alloc = device_data.get("rack_unit_allocations", device.rack_unit_allocations)
    #     BaseDeviceService._validate_and_allocate_rack(device, new_rack, new_start, new_alloc)

    #     # Apply rack allocation to the device
    #     device.rack = new_rack
    #     device.starting_position = new_start
    #     device.rack_unit_allocations = new_alloc

    #     # -----------------------
    #     # Update Device fields
    #     # -----------------------
    #     allowed_fields = [
    #         "name",
    #         "serial_number",
    #         "ipv4_address",
    #         "model",
    #         "weight",
    #         "power",
    #         "description",
    #         "interface_count",
    #     ]
    #     for field in allowed_fields:
    #         if field in device_data:
    #             setattr(device, field, device_data[field])

    #     device.save()  # 🔑 Save all updates to Device

    #     # -----------------------
    #     # Sync nested units and interfaces
    #     # -----------------------
    #     SwitchService._sync_units(device, nested_data)
    #     BaseDeviceService._handle_interfaces(device, nested_data, is_create=False)

    #     return device

