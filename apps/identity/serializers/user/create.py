# from rest_framework import serializers
# from django.contrib.auth.password_validation import validate_password

# class UserCreateSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)
#     email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)

#     department = serializers.UUIDField(required=False)

#     roles = serializers.ListField(
#         child=serializers.UUIDField(),
#         required=False,
#     )

#     policies = serializers.ListField(
#         child=serializers.UUIDField(),
#         required=False,
#     )

#     def validate_password(self, value):
#         validate_password(value)
#         return value

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from apps.identity.models import User

class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    department = serializers.UUIDField()
    roles = serializers.ListField(
        child=serializers.UUIDField(),
        required=True,
        allow_empty=False,
    )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

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