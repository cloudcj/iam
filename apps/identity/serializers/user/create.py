from rest_framework import serializers

class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    email = serializers.EmailField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )

    department = serializers.CharField()
    roles = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
    )
