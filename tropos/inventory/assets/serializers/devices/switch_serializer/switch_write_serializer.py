# from rest_framework import serializers
# from django.core.exceptions import ValidationError as DjangoValidationError
# from inventory.assets.models import Switch, Device
# from inventory.infrastructure.models import Rack
# from inventory.assets.services import SwitchService
# from ...components.psu_serializer import PowerSupplyUnitSerializer
# from ...components.fan_serializer import FanUnitSerializer

# class SwitchWriteSerializer(serializers.ModelSerializer):
#     # Device-related fields
#     rack_id = serializers.PrimaryKeyRelatedField(
#     queryset=Rack.objects.all(),
#     source="device.rack",
#     write_only=True,
#     required=False,  # optional for PATCH
#     )
#     serial_number = serializers.CharField(source="device.serial_number", write_only=True, required=False)
#     rack_unit_allocations = serializers.IntegerField(source="device.rack_unit_allocations", write_only=True, required=False)
#     rack_unit_starting_position = serializers.IntegerField(source="device.starting_position", write_only=True, required=False)
#     ipv4_address = serializers.CharField(source="device.ipv4_address", write_only=True, required=False)
#     model = serializers.CharField(source="device.model", write_only=True, required=False)
#     interface_count = serializers.IntegerField(source="device.interface_count", write_only=True, required=False)
#     weight = serializers.IntegerField(source="device.weight", write_only=True, required=False)
#     power = serializers.FloatField(source="device.power", write_only=True, required=False)
#     description = serializers.CharField(source="device.description", write_only=True, required=False)

#     # Nested units
#     power_supply_units = PowerSupplyUnitSerializer(many=True, write_only=True, required=False)
#     # fan_units = FanUnitSerializer(many=True, write_only=True, required=False)

#     class Meta:
#         model = Switch
#         fields = [
#             "rack_id",
#             "switch_name",
#             "model",
#             "serial_number",
#             "ipv4_address",
#             "rack_unit_allocations",
#             "rack_unit_starting_position",
#             "interface_count",
#             "weight",
#             "power",
#             "description",
#             "power_supply_units",
#             # "fan_units"
#         ]

#     # -----------------------
#     # Field-level Validations
#     # -----------------------

#     def validate_rack_unit_starting_position(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("starting_position must be a positive integer.")
#         return value

#     def validate_rack_unit_allocations(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("rack_unit_allocations must be a positive integer.")
#         return value

#     def validate_interface_count(self, value):
#         if value is not None and value < 0:
#             raise serializers.ValidationError("interface_count cannot be negative.")
#         return value

#     # -----------------------
#     # Combined Validation
#     # -----------------------

#     def validate(self, attrs):
#         device_data = attrs.get("device", {})

#         # For PATCH, fallback to existing values if not provided
#         rack = device_data.get("rack") or (self.instance.device.rack if self.instance else None)
#         start = device_data.get("starting_position") or (self.instance.device.starting_position if self.instance else None)
#         alloc = device_data.get("rack_unit_allocations") or (self.instance.device.rack_unit_allocations if self.instance else None)

#         # Required only on creation
#         if not rack and self.instance is None:
#             raise serializers.ValidationError("rack_id is required on creation.")
#         if self.instance is None and (start is None or alloc is None):
#             raise serializers.ValidationError("Both starting_position and rack_unit_allocations are required on creation.")

#         # Validate positions within rack limits
#         if rack and start is not None and alloc is not None:
#             end = start + alloc - 1
#             if hasattr(rack, "max_units") and end > rack.max_units:
#                 raise serializers.ValidationError(
#                     f"Requested positions exceed rack capacity (max {rack.max_units})."
#                 )

#         return attrs

#     # -----------------------
#     # Create / Update
#     # -----------------------

#     def create(self, validated_data):
#         device_data = validated_data.pop("device")
#         nested_data = {
#             "power_supply_units": validated_data.pop("power_supply_units", []),
#             "fan_units": validated_data.pop("fan_units", []),
#             "interface_count": validated_data.pop("interface_count", None),
#         }
#         try:
#             return SwitchService.create_switch(device_data, validated_data, nested_data)
#         except DjangoValidationError as e:
#             raise serializers.ValidationError(str(e))

#     def update(self, instance, validated_data):
#         device_data = validated_data.pop("device", {})
#         nested_data = {
#             "power_supply_units": validated_data.pop("power_supply_units", None),
#             "fan_units": validated_data.pop("fan_units", None),
#             "interface_count": validated_data.pop("interface_count", None),
#         }
#         try:
#             return SwitchService.update_switch(instance, device_data, validated_data, nested_data)
#         except DjangoValidationError as e:
#             raise serializers.ValidationError(str(e))


#-======================================================================


# assets/serializers/device/switch_write_serializer.py
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from inventory.assets.models import Switch, Device
from inventory.infrastructure.models import Rack
from inventory.assets.services.device.switch_service import SwitchService
from inventory.assets.services.rack.rack_service import RackService
from ...components.psu_serializer import PowerSupplyUnitSerializer
from ...components.fan_serializer import FanUnitSerializer


class SwitchWriteSerializer(serializers.ModelSerializer):
    # -----------------------
    # Device-related fields
    # -----------------------
    rack_id = serializers.PrimaryKeyRelatedField(
        queryset=Rack.objects.all(),
        source="device.rack",
        write_only=True,
        required=False,
    )
    name = serializers.CharField(source="device.name", write_only=True, required=False)
    model = serializers.CharField(source="device.model", write_only=True, required=False)
    serial_number = serializers.CharField(source="device.serial_number", write_only=True, required=False)
    rack_unit_allocations = serializers.IntegerField(source="device.rack_unit_allocations", write_only=True, required=False)
    rack_unit_starting_position = serializers.IntegerField(source="device.starting_position", write_only=True, required=False)
    ipv4_address = serializers.CharField(source="device.ipv4_address", write_only=True, required=False)
    model = serializers.CharField(source="device.model", write_only=True, required=False)
    interface_count = serializers.IntegerField(source="device.interface_count", write_only=True, required=False)
    weight = serializers.IntegerField(source="device.weight", write_only=True, required=False)
    power = serializers.FloatField(source="device.power", write_only=True, required=False)
    description = serializers.CharField(source="device.description", write_only=True, required=False)

    # -----------------------
    # Nested units
    # -----------------------
    power_supply_units = PowerSupplyUnitSerializer(many=True, write_only=True, required=False)
    fan_units = FanUnitSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Switch
        fields = [
            "rack_id",
            "name",
            "model",
            "serial_number",
            "ipv4_address",
            "rack_unit_allocations",
            "rack_unit_starting_position",
            "interface_count",
            "weight",
            "power",
            "description",
            "power_supply_units",
            "fan_units",
        ]

    # -----------------------
    # Field-level validations
    # -----------------------
    def validate_rack_unit_starting_position(self, value):
        if value <= 0:
            raise serializers.ValidationError("starting_position must be a positive integer.")
        return value

    def validate_rack_unit_allocations(self, value):
        if value <= 0:
            raise serializers.ValidationError("rack_unit_allocations must be a positive integer.")
        return value

    def validate_interface_count(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("interface_count cannot be negative.")
        return value

    # -----------------------
    # Combined validation
    # -----------------------
    def validate(self, attrs):
        device_data = attrs.get("device", {})

        rack = device_data.get("rack") or (
            self.instance.device.rack if self.instance else None
        )
        start = device_data.get("starting_position") or (
            self.instance.device.starting_position if self.instance else None
        )
        alloc = device_data.get("rack_unit_allocations") or (
            self.instance.device.rack_unit_allocations if self.instance else None
        )


        # Required only on creation
        if not rack and self.instance is None:
            raise serializers.ValidationError({"rack_id": "rack_id is required on creation."})
        if self.instance is None and (start is None or alloc is None):
            raise serializers.ValidationError({
                "rack_unit_allocations": "Both starting_position and rack_unit_allocations are required on creation."
            })

        # Use RackService for validation
        if rack and start is not None and alloc is not None:
            try:
                RackService.validate_positions(rack, start, alloc, exclude_device=(self.instance.device if self.instance else None))
            except DjangoValidationError as e:
                raise serializers.ValidationError(getattr(e, "message_dict", str(e)))

        return attrs

    # -----------------------
    # Create / Update
    # -----------------------
    def create(self, validated_data):
        device_data = validated_data.pop("device")
        nested_data = {
            "power_supply_units": validated_data.pop("power_supply_units", []),
            "fan_units": validated_data.pop("fan_units", []),
            "interface_count": validated_data.pop("interface_count", None),
        }
        try:
            return SwitchService.provision_switch(device_data, validated_data, nested_data)
        except DjangoValidationError as e:
            raise serializers.ValidationError(getattr(e, "message_dict", str(e)))
        
    def update(self, instance, validated_data):
        device_data = validated_data.pop("device", {})

        nested_data = {
            "power_supply_units": validated_data.pop("power_supply_units", None),
            "fan_units": validated_data.pop("fan_units", None),
            "interface_count": validated_data.pop("interface_count", None),
        }

        try:
            return SwitchService.reconfigure_switch(
                instance=instance,
                device_data=device_data,
                nested_data=nested_data,
            )
        except DjangoValidationError as e:
            raise serializers.ValidationError(
                getattr(e, "message_dict", str(e))
            )



    # def update(self, instance, validated_data):
    #     device_data = validated_data.pop("device", {})
    #     nested_data = {
    #         "power_supply_units": validated_data.pop("power_supply_units", None),
    #         "fan_units": validated_data.pop("fan_units", None),
    #         "interface_count": validated_data.pop("interface_count", None),
    #     }
    #     try:
    #         return SwitchService.reconfigure_switch(instance, device_data, validated_data, nested_data)
    #     except DjangoValidationError as e:
    #         raise serializers.ValidationError(getattr(e, "message_dict", str(e)))
