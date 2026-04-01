# from rest_framework import serializers
# from ..models import Area

# class AreaSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = Area
#     fields = ['id', 'location', 'created_at', 'updated_at']
#     read_only_fields = ["id", "created_at", "updated_at"]

# class AreaNestedSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = Area
#     fields = ['id', 'location']

from rest_framework import serializers
from ..models import AvailabilityZone, Region
from .region_serializer import RegionSerializer

class AZSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(source='region',queryset=Region.objects.all(), write_only=True)
    class Meta:
        model = AvailabilityZone
        fields = ['id', 'name', 'location', 'region', 'region_id', 'created_at', 'updated_at']
        read_only_fields = ['id','created_at', 'updated_at']

class AZSummarySerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = AvailabilityZone
        fields = ['id', 'name', 'location', 'region', 'created_at', 'updated_at']
        read_only_fields = ['id','created_at', 'updated_at']