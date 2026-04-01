from rest_framework import serializers
from ..models.appliance_type_enums import ApplianceType

class ApplianceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplianceType
        fields = ['id', 'name']

class ApplianceTypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplianceType
        fields = ['id', 'name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']