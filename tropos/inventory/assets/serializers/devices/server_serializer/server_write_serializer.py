# from rest_framework import serializers
# from django.core.exceptions import ValidationError as DjangoValidationError
# # Models
# from inventory.infrastructure.models import Rack
# from inventory.assets.models import Server
# # Services
# from inventory.assets.services import ServerService
# # Serializes
# from ...components import MemoryUnitWriteSerializer,ProcessorUnitWriteSerializer,StorageUnitWriteSerializer
# from ...components.psu_serializer import PowerSupplyUnitSerializer
# from ...components.fan_serializer import FanUnitSerializer


# class ServerWriteSerializer(serializers.ModelSerializer):

#     # Device fields
#     rack_id = serializers.PrimaryKeyRelatedField(
#         queryset=Rack.objects.all(),
#         source="device.rack",
#         write_only=True,
#         required=False,
#     )
#     serial_number = serializers.CharField(source="device.serial_number", write_only=True, required=False)
#     rack_unit_allocations = serializers.IntegerField(source="device.rack_unit_allocations", write_only=True, required=False)
#     rack_unit_starting_position = serializers.IntegerField(source="device.starting_position", write_only=True, required=False)
#     ipv4_address = serializers.CharField(source="device.ipv4_address", write_only=True, required=False)
#     interface_count = serializers.IntegerField(source="device.interface_count", write_only=True, required=False)
#     weight = serializers.IntegerField(source="device.weight", write_only=True, required=False)
#     power = serializers.FloatField(source="device.power", write_only=True, required=False)
#     description = serializers.CharField(source="device.description", write_only=True, required=False)

#     # Nested component lists
#     memory_units = MemoryUnitWriteSerializer(many=True, write_only=True, required=False)
#     processor_units = ProcessorUnitWriteSerializer(many=True, write_only=True, required=False)
#     storage_units = StorageUnitWriteSerializer(many=True, write_only=True, required=False)
#     power_supply_units = PowerSupplyUnitSerializer(many=True, write_only=True, required=False)
#     fan_units = FanUnitSerializer(many=True, write_only=True, required=False)

#     # Read-only device reference
#     device = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = Server
#         fields = [
#             "server_name",
#             "classification",
#             "serial_number",
#             "rack_id",
#             "rack_unit_starting_position",
#             "rack_unit_allocations",
#             "ipv4_address",
#             "interface_count",
#             "weight",
#             "power",
#             "description",
#             "memory_units",
#             "processor_units",
#             "storage_units",
#             "power_supply_units",
#             "fan_units",
#             "device",
#         ]

#     # --------------------------------------------------------
#     # VALIDATION
#     # --------------------------------------------------------
#     def validate(self, attrs):
#         device_data = attrs.get("device", {})

#         if self.instance:
#             device = self.instance.device
#             rack = device_data.get("rack", device.rack)
#             start = device_data.get("starting_position", device.starting_position)
#             alloc = device_data.get("rack_unit_allocations", device.rack_unit_allocations)
#         else:
#             rack = device_data.get("rack")
#             start = device_data.get("starting_position")
#             alloc = device_data.get("rack_unit_allocations")

#         if not rack and not self.instance:
#             raise serializers.ValidationError("rack_id is required on creation.")

#         if not self.instance and (start is None or alloc is None):
#             raise serializers.ValidationError(
#                 "Both rack_unit_starting_position and rack_unit_allocations are required on creation."
#             )

#         return attrs

#     # --------------------------------------------------------
#     # CREATE
#     # --------------------------------------------------------
#     def create(self, validated_data):
#         device_data = validated_data.pop("device", {})
#         nested_data = {
#             "memory_units": validated_data.pop("memory_units", []),
#             "processor_units": validated_data.pop("processor_units", []),
#             "storage_units": validated_data.pop("storage_units", []),
#             "power_supply_units": validated_data.pop("power_supply_units", []),
#             "fan_units": validated_data.pop("fan_units", []),
#             "interface_count": device_data.get("interface_count"),
#         }

#         try:
#             return ServerService.create_server(
#                 device_data=device_data,
#                 server_data=validated_data,
#                 nested_data=nested_data,
#             )
#         except DjangoValidationError as e:
#             raise serializers.ValidationError(str(e))

#     # --------------------------------------------------------
#     # UPDATE
#     # --------------------------------------------------------
#     def update(self, instance, validated_data):
#         device_data = validated_data.pop("device", {})
#         nested_data = {
#             "memory_units": validated_data.pop("memory_units", None),
#             "processor_units": validated_data.pop("processor_units", None),
#             "storage_units": validated_data.pop("storage_units", None),
#             "power_supply_units": validated_data.pop("power_supply_units", None),
#             "fan_units": validated_data.pop("fan_units", None),
#             "interface_count": device_data.get("interface_count"),
#         }

#         try:
#             return ServerService.update_server(
#                 instance=instance,
#                 device_data=device_data,
#                 server_data=validated_data,
#                 nested_data=nested_data,
#             )
#         except DjangoValidationError as e:
#             raise serializers.ValidationError(str(e))



#=====================================================================




# assets/serializers/device/server_write_serializer.py
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from inventory.assets.models import Server, Device
from inventory.infrastructure.models import Rack
from inventory.assets.services.device.server_service import ServerService
from inventory.assets.services.rack.rack_service import RackService
from ...components.compute_serializer.compute_write_serializer import MemoryUnitWriteSerializer
from ...components.compute_serializer.compute_write_serializer import ProcessorUnitWriteSerializer
from ...components.compute_serializer.compute_write_serializer import StorageUnitWriteSerializer
from ...components.psu_serializer import PowerSupplyUnitSerializer
from ...components.fan_serializer import FanUnitSerializer


class ServerWriteSerializer(serializers.ModelSerializer):
    # -----------------------
    # Device-related fields
    # -----------------------
    rack_id = serializers.PrimaryKeyRelatedField(
        queryset=Rack.objects.all(),
        source="device.rack",
        write_only=True,
        required=False,
    )
    serial_number = serializers.CharField(source="device.serial_number", write_only=True, required=False)
    name = serializers.CharField(source="device.name", write_only=True, required=False)
    model = serializers.CharField(source="device.model", write_only=True, required=False)
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
    memory_units = MemoryUnitWriteSerializer(many=True, write_only=True, required=False)
    processor_units = ProcessorUnitWriteSerializer(many=True, write_only=True, required=False)
    storage_units = StorageUnitWriteSerializer(many=True, write_only=True, required=False)
    power_supply_units = PowerSupplyUnitSerializer(many=True, write_only=True, required=False)
    fan_units = FanUnitSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Server
        fields = [
            "rack_id",
            "name",
            "classification",
            "model",
            "serial_number",
            "ipv4_address",
            "rack_unit_allocations",
            "rack_unit_starting_position",
            "interface_count",
            "weight",
            "power",
            "description",
            "memory_units",
            "processor_units",
            "storage_units",
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

        rack = device_data.get("rack") or (self.instance.device.rack if self.instance else None)
        start = device_data.get("starting_position") or (self.instance.device.starting_position if self.instance else None)
        alloc = device_data.get("rack_unit_allocations") or (self.instance.device.rack_unit_allocations if self.instance else None)

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
            "memory_units": validated_data.pop("memory_units", []),
            "processor_units": validated_data.pop("processor_units", []),
            "storage_units": validated_data.pop("storage_units", []),
            "power_supply_units": validated_data.pop("power_supply_units", []),
            "fan_units": validated_data.pop("fan_units", []),
            "interface_count": validated_data.pop("interface_count", None),
        }
        try:
            return ServerService.provision_server(device_data, validated_data, nested_data)
        except DjangoValidationError as e:
            raise serializers.ValidationError(getattr(e, "message_dict", str(e)))

    def update(self, instance, validated_data):
        device_data = validated_data.pop("device", {})
        nested_data = {
            "memory_units": validated_data.pop("memory_units", None),
            "processor_units": validated_data.pop("processor_units", None),
            "storage_units": validated_data.pop("storage_units", None),
            "power_supply_units": validated_data.pop("power_supply_units", None),
            "fan_units": validated_data.pop("fan_units", None),
            "interface_count": validated_data.pop("interface_count", None),
        }
        try:
            return ServerService.reconfigure_server(instance, device_data, validated_data, nested_data)
        except DjangoValidationError as e:
            raise serializers.ValidationError(getattr(e, "message_dict", str(e)))







