from rest_framework import serializers
from inventory.assets.models import PowerSupplyUnit


class PowerSupplyUnitSerializer(serializers.ModelSerializer):
  

    class Meta:
        model = PowerSupplyUnit
        fields = [
            "id",
            "max_output",
            "description"

        ]

class ShowAllPowerSupplyUnitSerializer(serializers.ModelSerializer):
    device_id = serializers.PrimaryKeyRelatedField(source='device', read_only=True)

    class Meta:
        model = PowerSupplyUnit
        fields = [
            "id",
            "device_id",
            "heat_dissipation",
            "max_output",
            "average_output",
            "wattage_percentage",
            "power_type",
            "connector_type",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ['created_at', 'updated_at']