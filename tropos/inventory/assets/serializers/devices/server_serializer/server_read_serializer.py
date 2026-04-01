from rest_framework import serializers
# Models
from inventory.assets.models import Server
from inventory.infrastructure.models import RackPosition
# Serializers
from ..device_serializer import DeviceSerializer,RackPositionSummarySerializer
from ...components.compute_serializer import MemoryUnitReadSerializer,ProcessorUnitReadSerializer,StorageUnitReadSerializer
from ...components.interface_serializer import InterfaceDetailSerializer
from ...components.psu_serializer import ShowAllPowerSupplyUnitSerializer
from ...components.fan_serializer import FanUnitSerializer 



class ServerSummarySerializer(serializers.ModelSerializer):
    # device_id = serializers.IntegerField(source="device.id", read_only=True)
    # device = serializers.SerializerMethodField()
    device = DeviceSerializer(read_only=True)
    class Meta:
        model = Server
        fields = [
            # "device_id",
            # "server_name",
            "classification",
            "device",
        ]

    # def get_device(self, obj):
    #     return {
    #         "type": obj.device.type,
    #         "rack": {
    #             "number": obj.device.rack.number,
    #         } if obj.device.rack else None
    #     }
    
class ServerDetailSerializer(serializers.ModelSerializer):
    # device_id = serializers.IntegerField(source="device.id", read_only=True)
    # device = serializers.SerializerMethodField()
    device = DeviceSerializer(read_only=True)
    memory_units = MemoryUnitReadSerializer(source="device.memory_units", many=True, read_only=True)
    processor_units = ProcessorUnitReadSerializer(source="device.processor_units", many=True, read_only=True)
    storage_units = StorageUnitReadSerializer(source="device.storage_units", many=True, read_only=True)

    class Meta:
        model = Server
        fields = [
            # "device_id",
            # "server_name",
            "classification",
            "device",
            "memory_units",
            "processor_units",
            "storage_units",
        ]

    # def get_device(self, obj):
    #     return {
    #         "type": obj.device.type,
    #         "rack": {
    #             "number": obj.device.rack.number,
    #         } if obj.device.rack else None
    #     }



# # ----------------------
# # Server Detail Serializer
# # ----------------------
# class ServerDetailSerializer(serializers.ModelSerializer):
#     device_id = serializers.IntegerField(source="device.id", read_only=True)
#     device = serializers.SerializerMethodField()

#     interfaces = InterfaceDetailSerializer(source="device.interfaces", many=True, read_only=True)
#     power_supply_units = ShowAllPowerSupplyUnitSerializer(source="device.power_supply_units", many=True, read_only=True)
#     fan_units = FanUnitSerializer(source="device.fan_units", many=True, read_only=True)
#     memory_units = MemoryUnitReadSerializer(source="device.memory_units", many=True, read_only=True)
#     processor_units = ProcessorUnitReadSerializer(source="device.processor_units", many=True, read_only=True)
#     storage_units = StorageUnitReadSerializer(source="device.storage_units", many=True, read_only=True)

#     class Meta:
#         model = Server
#         fields = [
#             "device_id",
#             "server_name",
#             "serial_number",
#             "classification",
#             "server_area",
#             "node_name",
#             "rack_unit_allocations",
#             "rack_unit_starting_position",
#             "description",
#             "device",
#             "power_supply_units",
#             "fan_units",
#             "interfaces",
#             "memory_units",
#             "processor_units",
#             "storage_units",
#         ]

#     def get_device(self, obj):
#         return {
#             "rack": {
#                 "id": obj.device.rack.id,
#                 "number": obj.device.rack.number,
#             } if obj.device.rack else None,
#             "positions": RackPositionSummarySerializer(
#                 RackPosition.objects.filter(device=obj.device),
#                 many=True
#             ).data
#         }
