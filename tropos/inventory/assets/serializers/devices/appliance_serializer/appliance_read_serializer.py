from rest_framework import serializers
from inventory.assets.models import Appliance
from inventory.enums.serializers.appliance_type_serializer import ApplianceTypeSerializer
from ..device_serializer.device_serializer import DeviceSerializer
from ...components.compute_serializer import (
    MemoryUnitWriteSerializer,
    ProcessorUnitWriteSerializer,
    StorageUnitWriteSerializer
)
from ...components.psu_serializer import PowerSupplyUnitSerializer
from ...components.fan_serializer import FanUnitSerializer
from .appliance_chassis_serializer import ApplianceChassisDetailSerializer


class ApplianceSummarySerializer(serializers.ModelSerializer):
    appliance_type = ApplianceTypeSerializer(read_only=True)
    device = DeviceSerializer(read_only=True)

    class Meta:
        model = Appliance
        fields = [
            # "appliance_name",
            # "model",  
            "appliance_type",
            "device",
            "is_chassis",
            "has_components_units",
        ]


class ApplianceDetailSerializer(serializers.ModelSerializer):
    appliance_type = ApplianceTypeSerializer(read_only=True)
    device = DeviceSerializer(read_only=True)

    # Include nested components
    memory_units = MemoryUnitWriteSerializer(many=True, source="device.memory_units", read_only=True)
    processor_units = ProcessorUnitWriteSerializer(many=True, source="device.processor_units", read_only=True)
    storage_units = StorageUnitWriteSerializer(many=True, source="device.storage_units", read_only=True)
    # power_supply_units = PowerSupplyUnitSerializer(many=True, source="device.power_supply_units", read_only=True)
    # fan_units = FanUnitSerializer(many=True, source="device.fan_units", read_only=True)
    appliance_chassis = ApplianceChassisDetailSerializer(many=True, source="device.chasis_modules", read_only=True)

    class Meta:
        model = Appliance
        fields = [
            # "appliance_name",
            "model",  
            "appliance_type",
            "device",
            "is_chassis",
            "has_components_units",
            "memory_units",
            "processor_units",
            "storage_units",
            # "power_supply_units",
            # "fan_units",
            "appliance_chassis",
        ]






# class ApplianceSummarySerializer(serializers.ModelSerializer):
#     appliance_type = ApplianceTypeSerializer(read_only=True)
#     serial_number = serializers.CharField(source="device.serial_number", read_only=True)
#     rack_unit_allocations = serializers.IntegerField(source="device.rack_unit_allocations", read_only=True)
#     rack_unit_starting_position = serializers.IntegerField(source="device.starting_position", read_only=True)
#     ipv4_address = serializers.CharField(source="device.ipv4_address", read_only=True)
#     weight = serializers.FloatField(source="device.weight", read_only=True)
#     power = serializers.FloatField(source="device.power", read_only=True)
#     status = serializers.CharField(source="device.status", read_only=True)
#     interface_count = serializers.IntegerField(source="device.interface_count", read_only=True)
#     deleted_at = serializers.DateTimeField(source="device.deleted_at", read_only=True)

#     class Meta:
#         model = Appliance
#         fields = [
#             "id",
#             "appliance_type",
#             "appliance_name",
#             "is_chassis",
#             "description",
#             "serial_number",
#             "rack_unit_allocations",
#             "rack_unit_starting_position",
#             "ipv4_address",
#             "weight",
#             "power",
#             "status",
#             "interface_count",
#             "deleted_at",
#         ]









# # ----------------------
# # Appliance Summary Serializer
# # ----------------------
# class ApplianceSummarySerializer(serializers.ModelSerializer):
#     appliance_type = ApplianceTypeSerializer(read_only=True)

#     class Meta:
#         model = Appliance
#         fields = [
#             "id",
#             "device",
#             "appliance_type",
#             "appliance_name",
#             "is_chassis",
#             "serial_number",
#             "rack_unit_allocations",
#             "rack_unit_starting_position",
#         ]


# # ----------------------
# # Appliance Detail Serializer
# # ----------------------
# class ApplianceDetailSerializer(serializers.ModelSerializer):
#     appliance_type = ApplianceTypeDetailSerializer(read_only=True)
#     device = DeviceSerializer(read_only=True)

#     # Nested units
#     memory_units = MemoryUnitReadSerializer(source="device.memory_units", many=True, read_only=True)
#     processor_units = ProcessorUnitReadSerializer(source="device.processor_units", many=True, read_only=True)
#     storage_units = StorageUnitReadSerializer(source="device.storage_units", many=True, read_only=True)

#     # PSU, fans, interfaces
#     power_supply_units = ShowAllPowerSupplyUnitSerializer(source="device.power_supply_units", many=True, read_only=True)
#     fan_units = FanUnitSerializer(source="device.fan_units", many=True, read_only=True)
#     interfaces = InterfaceDetailSerializer(source="device.interfaces", many=True, read_only=True)

#     # Chassis modules
#     appliance_chassis = ApplianceChassisDetailSerializer(source="device.chasis_modules", many=True, read_only=True)

#     class Meta:
#         model = Appliance
#         fields = [
#             "id",
#             "device",
#             "appliance_type",
#             "appliance_name",
#             "is_chassis",
#             "serial_number",
#             "rack_unit_allocations",
#             "rack_unit_starting_position",
#             "processor_units",
#             "memory_units",
#             "storage_units",
#             "power_supply_units",
#             "fan_units",
#             "appliance_chassis",
#             "interfaces",
#             "description",
#             "created_at",
#             "updated_at",
#         ]
#         read_only_fields = ["created_at", "updated_at"]
