from rest_framework import serializers
from ..models import Building, AvailabilityZone
from .az_serializer import AZSerializer


class BuildingSerializer(serializers.ModelSerializer):
  availability_zone = AZSerializer(read_only=True)
  availability_zone_id = serializers.PrimaryKeyRelatedField(
    source="availability_zone",
    queryset=AvailabilityZone.objects.all(),
    write_only=True
  )
  class Meta:
        model = Building
        fields = ['id','name','availability_zone_id', 'availability_zone','created_at', 'updated_at']
        read_only_fields = ["id", "created_at", "updated_at"]

class BuildingSummarySerializer(serializers.ModelSerializer):
  class Meta:
    model = Building
    fields = ['id', 'name']