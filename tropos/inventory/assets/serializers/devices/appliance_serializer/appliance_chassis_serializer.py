# assets/serializers/appliance_chasis_serializer.py
from rest_framework import serializers
from inventory.assets.models import ApplianceChassis
from ...components.interface_serializer import InterfaceDetailSerializer as InterfaceSerializer 


# ----------------------
# Summary Serializer (list view)
# ----------------------
class ApplianceChassisSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplianceChassis
        fields = [
            "id",
            "device",
            "module_name",
            "module_count",
        ]


# ----------------------
# Detail Serializer (retrieve view)
# ----------------------
class ApplianceChassisDetailSerializer(serializers.ModelSerializer):
    interfaces = InterfaceSerializer(source="device.interfaces", many=True, read_only=True)

    class Meta:
        model = ApplianceChassis
        fields = [
            "id",
            "module_name",
            "serial_number",
            "is_occupied",
            "slot_position",
            "interfaces",
            # "created_at",
            # "updated_at",
        ]
        # read_only_fields = ["created_at", "updated_at"]
