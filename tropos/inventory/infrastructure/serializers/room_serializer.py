from rest_framework import serializers
from ..models import Room, Floor
from .floor_serializer import FloorNestedSerializer
from .building_serializer import BuildingSummarySerializer

class RoomSerializer(serializers.ModelSerializer):
  floor = FloorNestedSerializer(read_only=True)
  floor_id = serializers.PrimaryKeyRelatedField(
    source='floor',
    queryset=Floor.objects.all(),
    write_only=True
  )
  # building_name=serializers.CharField(source="building.name",read_only=True)
  building = BuildingSummarySerializer(source="floor.building", read_only=True)

  class Meta:
    model = Room
    fields = ['id', 'floor_id', 'floor', 'number','building', 'created_at', 'updated_at']
    read_only_fields = ["id", "created_at", "updated_at"]

class RoomNestedSerializer(serializers.ModelSerializer):
  class Meta:
    model = Room
    fields = ['id', 'number']