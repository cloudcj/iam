from rest_framework import serializers
from django.db import transaction
from inventory.infrastructure.models import Rack
from inventory.assets.models import Appliance, Type
from inventory.assets.services import ApplianceService
from django.core.exceptions import ValidationError as DjangoValidationError

from ...components.psu_serializer import PowerSupplyUnitSerializer
from ...components.fan_serializer import FanUnitSerializer
from .appliance_chassis_serializer import ApplianceChassisDetailSerializer
from ...components.compute_serializer import (
    MemoryUnitWriteSerializer,
    ProcessorUnitWriteSerializer,
    StorageUnitWriteSerializer
)


class ApplianceWriteSerializer(serializers.ModelSerializer):
    # Device fields
    rack_id = serializers.PrimaryKeyRelatedField(
        queryset=Rack.objects.all(),
        source="device.rack",
        write_only=True,
        required=False,
    )
    name = serializers.CharField(source="device.name", write_only=True)
    model = serializers.CharField(write_only=True, required=False)  
    serial_number = serializers.CharField(source="device.serial_number", write_only=True, required=False)
    rack_unit_starting_position = serializers.IntegerField(source="device.starting_position", write_only=True, required=False)
    rack_unit_allocations = serializers.IntegerField(source="device.rack_unit_allocations", write_only=True, required=False)
    ipv4_address = serializers.CharField(source="device.ipv4_address", write_only=True, required=False)
    interface_count = serializers.IntegerField(source="device.interface_count", write_only=True, required=False)
    weight = serializers.FloatField(source="device.weight", write_only=True, required=False)
    power = serializers.FloatField(source="device.power", write_only=True, required=False)
    description = serializers.CharField(source="device.description", write_only=True, required=False)

    # Appliance model field
    
    # Nested component lists
    memory_units = MemoryUnitWriteSerializer(many=True, write_only=True, required=False)
    processor_units = ProcessorUnitWriteSerializer(many=True, write_only=True, required=False)
    storage_units = StorageUnitWriteSerializer(many=True, write_only=True, required=False)
    power_supply_units = PowerSupplyUnitSerializer(many=True, write_only=True, required=False)
    fan_units = FanUnitSerializer(many=True, write_only=True, required=False)
    appliance_chassis = ApplianceChassisDetailSerializer(many=True, write_only=True, required=False)

    # Read-only device reference
    device = serializers.PrimaryKeyRelatedField(read_only=True)
    has_components_units = serializers.BooleanField(read_only=True)

    class Meta:
        model = Appliance
        fields = [
            "name",
            "model",  
            "appliance_type",
            "is_chassis",
            "has_components_units",
            "serial_number",
            "rack_id",
            "rack_unit_starting_position",
            "rack_unit_allocations",
            "ipv4_address",
            "interface_count",
            "weight",
            "power",
            "description",
            "memory_units",
            "processor_units",
            "storage_units",
            "power_supply_units",
            "fan_units",
            "appliance_chassis",
            "device",
        ]

    # Validation
    def validate(self, attrs):
        device_data = attrs.get("device", {})
        if self.instance:
            device = self.instance.device
            rack = device_data.get("rack", device.rack)
            start = device_data.get("starting_position", device.starting_position)
            alloc = device_data.get("rack_unit_allocations", device.rack_unit_allocations)
        else:
            rack = device_data.get("rack")
            start = device_data.get("starting_position")
            alloc = device_data.get("rack_unit_allocations")

        if not rack and not self.instance:
            raise serializers.ValidationError("rack_id is required on creation.")
        if not self.instance and (start is None or alloc is None):
            raise serializers.ValidationError(
                "Both rack_unit_starting_position and rack_unit_allocations are required on creation."
            )
        return attrs

    # Helper to compute if appliance has components
    def _compute_has_components_units(self, nested_data):
        return any([
            nested_data.get("memory_units"),
            nested_data.get("processor_units"),
            nested_data.get("storage_units"),
            nested_data.get("power_supply_units"),
            nested_data.get("fan_units"),
            nested_data.get("appliance_chassis"),
        ])

    # CREATE
    @transaction.atomic
    def create(self, validated_data):
        device_data = validated_data.pop("device", {})
        device_data["type"] = Type.APPLIANCE

        nested_data = {
            "memory_units": validated_data.pop("memory_units", []),
            "processor_units": validated_data.pop("processor_units", []),
            "storage_units": validated_data.pop("storage_units", []),
            "power_supply_units": validated_data.pop("power_supply_units", []),
            "fan_units": validated_data.pop("fan_units", []),
            "appliance_chassis": validated_data.pop("appliance_chassis", []),
            "interface_count": device_data.get("interface_count"),
        }

        # Automatically set has_components_units
        validated_data["has_components_units"] = self._compute_has_components_units(nested_data)

        try:
            return ApplianceService.provision_appliance(
                device_data=device_data,
                appliance_data=validated_data,
                nested_data=nested_data,
            )
        except DjangoValidationError as e:
            raise serializers.ValidationError(str(e))

    # UPDATE
    @transaction.atomic
    def update(self, instance, validated_data):
        device_data = validated_data.pop("device", {})
        nested_data = {
            "memory_units": validated_data.pop("memory_units", None),
            "processor_units": validated_data.pop("processor_units", None),
            "storage_units": validated_data.pop("storage_units", None),
            "power_supply_units": validated_data.pop("power_supply_units", None),
            "fan_units": validated_data.pop("fan_units", None),
            "appliance_chassis": validated_data.pop("appliance_chassis", None),
            "interface_count": device_data.get("interface_count"),
        }

        # Automatically update has_components_units if nested data is provided
        validated_data["has_components_units"] = self._compute_has_components_units(nested_data)

        try:
            return ApplianceService.reconfigure_appliance(
                instance=instance,
                device_data=device_data,
                appliance_data=validated_data,
                nested_data=nested_data,
            )
        except DjangoValidationError as e:
            raise serializers.ValidationError(str(e))
