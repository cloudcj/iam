from rest_framework import serializers
from django.utils import timezone

class TimestampedSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return timezone.localtime(obj.created_at).strftime("%Y-%m-%d %H:%M:%S")

    def get_updated_at(self, obj):
        return timezone.localtime(obj.updated_at).strftime("%Y-%m-%d %H:%M:%S")
