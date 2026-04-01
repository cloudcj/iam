from rest_framework import serializers
from inventory.assets.models import TransceiverUnit
from inventory.assets.models import Interface
from inventory.enums.models.transceiver_type_enums import TransceiverType
from inventory.enums.serializers.transceiver_type_serializer import TransceiverTypeSerializer

class TransceiverUnitSerializer(serializers.ModelSerializer):
    transceiver_type = TransceiverTypeSerializer(read_only=True)
    transceiver_type_id = serializers.PrimaryKeyRelatedField(
        queryset=TransceiverType.objects.all(),
        source='transceiver_type',
        write_only=True
    )
    interface_id = serializers.PrimaryKeyRelatedField(
        queryset=Interface.objects.all(),
        source='interface',
        write_only=True
    )

    class Meta:
        model = TransceiverUnit
        fields = [
            "id",
            "interface_id",
            "transceiver_type",
            "transceiver_type_id",
        ]
        read_only_fields = ["id", "transceiver_type"]
