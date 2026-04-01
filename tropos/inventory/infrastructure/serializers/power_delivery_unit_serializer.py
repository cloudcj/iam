from rest_framework import serializers
from ..models import PowerDeliveryUnit, PowerDeliveryUnitOutlet
from .rack_serializer import RackNestedSerializer

class PowerDeliveryUnitSerializer(serializers.ModelSerializer):
  rack = RackNestedSerializer(read_only=True)

  class Meta:
    model = PowerDeliveryUnit
    fields = ['id', 'rack', 'position', 'max_output', 'description', 'created_at', 'updated_at']
    read_only_fields = ['id', 'created_at', 'updated_at']

  def validate(self, attrs):
    request = self.context.get('request')
    if request and request.method == 'PATCH':
      allowed_fields = {"max_output", "description"}

      # Ensure no disallowed fields are updated
      if set(attrs.keys()) - allowed_fields:
        raise serializers.ValidationError(
          {"required_fields": "Only 'max_output' and 'description' can be updated."}
        )

      # Require at least one of them
      if not any(field in attrs for field in allowed_fields):
        raise serializers.ValidationError(
          {"required_fields": "At least one of 'max_output' or 'description' must be provided."}
        )
    return attrs

class PowerDeliveryUnitNestedSerializer(serializers.ModelSerializer):
  class Meta:
    model = PowerDeliveryUnit
    fields = ['id', 'position']

class PowerDeliveryUnitOutletSerializer(serializers.ModelSerializer):
  power_delivery_unit = PowerDeliveryUnitNestedSerializer(read_only=True)
  pdu_id = serializers.PrimaryKeyRelatedField(
    source='power_delivery_unit',
    queryset=PowerDeliveryUnit.objects.all(),
    write_only=True
  )
  class Meta:
    model = PowerDeliveryUnitOutlet
    fields = [
      'id', 
      'pdu_id',
      'power_delivery_unit', 
      'outlet_number', 
      'to_location', 
      'description',
      'created_at',
      'updated_at',
      ]
    read_only_fields = ['id', 'created_at', 'updated_at']
    