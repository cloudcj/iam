from rest_framework import serializers
from inventory.assets.models import FanUnit

class FanUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = FanUnit
        fields = [
            "id",
            "fan_count",
        ]
        

class ShowAllFanUnitSerializer(serializers.ModelSerializer):
    device_id = serializers.PrimaryKeyRelatedField(source='device', read_only=True)

    class Meta:
        model = FanUnit
        fields = [
            "id",
            "device_id",
            "fan_count",
            "fan_speed",
            "is_internal",
            "wattage_max_output",
            "wattage_average",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ['created_at', 'updated_at']