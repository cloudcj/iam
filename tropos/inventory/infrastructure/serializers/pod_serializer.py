from rest_framework import serializers
from ..models import Pod, Room
from .room_serializer import RoomNestedSerializer
from .building_serializer import BuildingSummarySerializer

class PodSerializer(serializers.ModelSerializer):
  room = RoomNestedSerializer(read_only=True)
  room_id = serializers.PrimaryKeyRelatedField(
    source="room",
    queryset=Room.objects.all(),
    write_only=True
  )
  building = BuildingSummarySerializer(source='room.floor.building',read_only=True)
  class Meta:
    model = Pod
    fields = ['id', 'room_id', 'room', 'name','building', 'created_at', 'updated_at']
    read_only_fields = ["id", "created_at", "updated_at"]

class PodNestedSerializer(serializers.ModelSerializer):
  class Meta:
    model = Pod
    fields = ['id', 'name']