from rest_framework import serializers
from inventory.assets.models import Interface
from .transceiver_unit_serializer import TransceiverUnitSerializer

class InterfaceDetailSerializer(serializers.ModelSerializer):
    device_id = serializers.PrimaryKeyRelatedField(source='device', read_only=True)
    # Include related transceivers
    transceiver_units = TransceiverUnitSerializer(many=True, read_only=True)

    class Meta:
        model = Interface
        fields = [
            "id",
            "device_id",
            "interface_number",
            "to_location",
            "cable_type",
            "port_type",
            "transceiver_units", 
            "description",
        ]


# Summary serializer for list view (show only selected fields)
class InterfaceSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Interface
        fields = [
            "id",
            "interface_number",
            "port_type",
        ]





# from rest_framework import serializers
# from ...models import Interface
# from .transceiver_unit_serializer import TransceiverUnitSerializer

# class ShowAllInterfaceSerializer(serializers.ModelSerializer):
#     device_id = serializers.PrimaryKeyRelatedField(source='device', read_only=True)
#     # Include related transceivers
#     transceiver_units = TransceiverUnitSerializer(many=True, read_only=True)

#     class Meta:
#         model = Interface
#         fields = [
#             "id",
#             "device_id",
#             "interface_number",
#             "to_location",
#             "cable_type",
#             "port_type",
#             "transceiver_units", 
#             "description",
#         ]


# # Summary serializer for list view (show only selected fields)
# class ShowSummaryInterfaceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Interface
#         fields = [
#             "id",
#             "interface_number",
#             "port_type",
#         ]
