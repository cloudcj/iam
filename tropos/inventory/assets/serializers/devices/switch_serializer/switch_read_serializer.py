
from rest_framework import serializers
from inventory.assets.models import Switch, Device
from ..device_serializer import DeviceSerializer

# class SwitchSummarySerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Device
#         fields = [
#             "id",
#             "name",
#             "serial_number",
#             "model",
#             "rack",
#             "rack_unit_allocations",
#             "starting_position",
#             "ipv4_address",
#             "weight",
#             "power",
#             "status",
#             "interface_count",
#             "description",
#         ]

class SwitchSummarySerializer(serializers.ModelSerializer):
    device = DeviceSerializer(read_only=True)

    class Meta:
        model = Switch
        fields = ['device']
