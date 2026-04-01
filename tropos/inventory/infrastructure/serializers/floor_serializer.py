from rest_framework import serializers
from ..models import Floor, Building
from .building_serializer import BuildingSummarySerializer

class FloorSerializer(serializers.ModelSerializer):
  building = BuildingSummarySerializer(read_only=True)
  building_id = serializers.PrimaryKeyRelatedField(
    source="building",
    queryset=Building.objects.all(),
    write_only=True
  )
  class Meta:
    model = Floor
    fields = ['id', 'building_id', 'building', 'number', 'created_at', 'updated_at']
    read_only_fields = ["id", "created_at", "updated_at"]

class FloorNestedSerializer(serializers.ModelSerializer):
  class Meta:
    model = Floor
    fields = ['id', 'number']