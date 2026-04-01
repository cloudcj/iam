from rest_framework import serializers
from ..models import Region

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name','created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']