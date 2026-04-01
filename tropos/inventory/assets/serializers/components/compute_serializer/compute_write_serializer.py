from rest_framework import serializers
from inventory.assets.models import MemoryUnit, ProcessorUnit, StorageUnit
from inventory.enums.models import StorageType, ProcessorCodename, ProcessorModel, ProcessorTier

# MEMORY UNIT
class MemoryUnitWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryUnit
        fields = ["id", "ram_capacity", "quantity"]

    # def validate(self, data):
    #     device = data["device"]
    #     if device.device_type not in ["server", "appliance"]:
    #         raise serializers.ValidationError(
    #             "Only servers and appliances may have memory units."
    #         )
    #     return data

# PROCESSOR UNIT
class ProcessorUnitWriteSerializer(serializers.ModelSerializer):
    processor_codename = serializers.PrimaryKeyRelatedField(queryset=ProcessorCodename.objects.all(),required=False)
    processor_tier = serializers.PrimaryKeyRelatedField(queryset=ProcessorTier.objects.all(),required=False)
    processor_model = serializers.PrimaryKeyRelatedField(queryset=ProcessorModel.objects.all(),required=False)

    class Meta:
        model = ProcessorUnit
        fields = [
            "id",
            "processor_codename",
            "processor_tier",
            "processor_model",
        ]

    # def validate(self, data):
    #     device = data["device"]
    #     if device.device_type not in ["server", "appliance","analyzer"]:
    #         raise serializers.ValidationError(
    #             "Only servers and appliances may have processor units."
    #         )
    #     return data

# STORAGE UNIT
class StorageUnitWriteSerializer(serializers.ModelSerializer):
    storage_type = serializers.ChoiceField(choices=StorageType.choices)

    class Meta:
        model = StorageUnit
        fields = ["id",
                  "storage_type",
                  "storage_interface",
                  "form_factor",
                  "storage_capacity",
                  "storage_count",
                  "capacity_unit"]
        
    # def validate(self, data):
    #     device = data["device"]
    #     if device.device_type not in ["server", "appliance"]:
    #         raise serializers.ValidationError(
    #             "Only servers and appliances may have storage units."
    #         )
    #     return data