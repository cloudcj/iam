from rest_framework import serializers

from inventory.assets.models import MemoryUnit, ProcessorUnit, StorageUnit
from inventory.enums.models import StorageType



class MemoryUnitReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryUnit
        fields = ["id", "ram_capacity", "quantity"]


class ProcessorUnitReadSerializer(serializers.ModelSerializer):
    processor_codename = serializers.SerializerMethodField()
    processor_tier = serializers.SerializerMethodField()
    processor_model = serializers.SerializerMethodField()

    class Meta:
        model = ProcessorUnit
        fields = ["id", "processor_codename", "processor_tier", "processor_model"]
    
    def get_processor_codename(self, obj):
        if obj.processor_codename:
            return {"id": obj.processor_codename.id, "name": obj.processor_codename.name}
        return None

    def get_processor_tier(self, obj):
        if obj.processor_tier:
            return {"id": obj.processor_tier.id, "name": obj.processor_tier.name}
        return None

    def get_processor_model(self, obj):
        if obj.processor_model:
            return {"id": obj.processor_model.id, "name": obj.processor_model.name}
        return None


class StorageUnitReadSerializer(serializers.ModelSerializer):
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
