from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)

    department = serializers.UUIDField(required=False)

    roles = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
    )

    policies = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
    )

    def validate_password(self, value):
        validate_password(value)
        return value

# class UserCreateSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)
#     email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
#     department = serializers.CharField()

#     roles = serializers.ListField(
#         child=serializers.CharField(),
#         required=False,
#     )

#     policies = serializers.ListField(
#         child=serializers.CharField(),
#         required=False,
#     )

#     def validate_password(self, value):
#         validate_password(value)
#         return value

#     def validate(self, data):
#         roles = data.get("roles") or []
#         policies = data.get("policies") or []

#         if not roles and not policies:
#             raise serializers.ValidationError(
#                 "At least one role or policy is required"
#             )

#         data["roles"] = roles
#         data["policies"] = policies

#         return data