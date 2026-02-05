from rest_framework import serializers


class UpdateUserBasicSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    is_active = serializers.BooleanField(required=False)


class UpdateUserDepartmentSerializer(serializers.Serializer):
    department = serializers.CharField()

class UpdateUserRolesSerializer(serializers.Serializer):
    roles = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
    )
