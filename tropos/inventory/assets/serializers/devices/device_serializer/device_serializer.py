from rest_framework import serializers
from inventory.assets.models import Device
from inventory.infrastructure.models import RackPosition


class RackPositionSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = RackPosition
        fields = ['id', 'position_number']



class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            "id",
            "type",
            "name",
            "serial_number",
            "model",
            "rack",
            "rack_unit_allocations",
            "starting_position",
            "ipv4_address",
            "weight",
            "power",
            "status",
            "interface_count",
            "description",
        ]


class DeviceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            "id",
            "type",
            "name",
            "serial_number",
            "model",
            "rack",
            "rack_unit_allocations",
            "starting_position",
            "ipv4_address",
            "weight",
            "power",
            "status",
            "interface_count",
            "description",
            "deleted_at",
            "created_at",
            "updated_at",
        ]



# from rest_framework import serializers
# from ...models import Device
# from inventory.infrastructure.models import Rack, RackPosition
# from inventory.infrastructure.serializers.rack_serializer import RackNestedSerializer
# from ..interface_serializer.interface_serializer import ShowAllInterfaceSerializer, ShowSummaryInterfaceSerializer  # import both

# class RackPositionSummarySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RackPosition
#         fields = ['id', 'position_number']

# class DeviceSerializer(serializers.ModelSerializer):
#     rack = RackNestedSerializer(read_only=True)
#     rack_id = serializers.PrimaryKeyRelatedField(source='rack', queryset=Rack.objects.all(), write_only=True)
#     positions = RackPositionSummarySerializer(many=True, read_only=True, source='rack_positions')
#     number_of_interfaces = serializers.IntegerField(read_only=True)
    
#     # Interfaces field (full by default)
#     interfaces = ShowAllInterfaceSerializer(many=True, read_only=True)
#     interface_count = serializers.IntegerField(write_only=True, required=False)
#     fan_count = serializers.SerializerMethodField()
#     status = serializers.CharField(source='get_status_display', read_only=True)
    
#     class Meta:
#         model = Device
#         fields = [
#             'id',
#             'rack_id', 'rack',
#             'type',
#             'status',             
#             'interface_count',    
#             'number_of_interfaces',
#             'positions',
#             'interfaces',
#             'fan_count',
#             'created_at',
#             'updated_at',
#         ]
#         read_only_fields = ['id', 'created_at', 'updated_at']

#     def get_fan_count(self, obj):
#         return sum(fan.fan_count for fan in obj.fan_units.all())

#     def to_representation(self, instance):
#         rep = super().to_representation(instance)
#         request = self.context.get("request")
#         if request and request.parser_context and request.parser_context['view'].action == 'list':
#             rep['interfaces'] = ShowSummaryInterfaceSerializer(instance.interfaces.all(), many=True).data
#         return rep
