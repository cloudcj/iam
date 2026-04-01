from rest_framework import serializers
from ..models import Rack, RackPosition, Pod
from inventory.assets.models import Device
from .pod_serializer import PodNestedSerializer

class RackSerializer(serializers.ModelSerializer):
  pod = PodNestedSerializer(read_only=True)
  pod_id = serializers.PrimaryKeyRelatedField(
    source="pod",
    queryset=Pod.objects.all(),
    write_only=True
  )
  class Meta:
    model = Rack
    fields = ['id', 'pod_id', 'pod', 'number','network_area','network_area_order', 'ru_count', 'weight', 'is_occupied', 'created_at', 'updated_at']
    read_only_fields = ['id', 'created_at', 'updated_at']

# Nested Rack Serializer
class RackNestedSerializer(serializers.ModelSerializer):
  class Meta:
    model = Rack
    fields = ['id', 'number']

class RackPositionSerializer(serializers.ModelSerializer):
  rack = RackNestedSerializer(read_only=True)
  device_id = serializers.PrimaryKeyRelatedField(
    source="device",
    queryset=Device.objects.all(),
    allow_null=True,
  )

  class Meta:
    model = RackPosition
    fields = ['id', 'rack', 'position_number', 'is_occupied', 'device_id', 'created_at', 'updated_at']
    read_only_fields = ['id', 'created_at', 'updated_at']

  def validate(self, attrs):
    request = self.context.get('request')
    if request and request.method == 'PATCH':
      if "device" not in attrs:
        raise serializers.ValidationError({"device_id": "This field is required."})
      if set(attrs.keys()) - {"device"}:
        raise serializers.ValidationError("Only 'device_id' can be updated.")
    return attrs