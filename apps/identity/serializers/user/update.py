# from rest_framework import serializers


# class UpdateUserBasicSerializer(serializers.Serializer):
#     email = serializers.EmailField(
#         required=False,
#         allow_null=True,
#         allow_blank=True,
#     )
#     is_active = serializers.BooleanField(required=False)


# class UpdateUserDepartmentSerializer(serializers.Serializer):
#     department = serializers.CharField()

# class UpdateUserRolesSerializer(serializers.Serializer):
#     roles = serializers.ListField(
#         child=serializers.CharField(),
#         allow_empty=False,
#     )


from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UpdateUserBasicSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    is_active = serializers.BooleanField(required=False)

class UpdateUserDepartmentSerializer(serializers.Serializer):
    department = serializers.CharField()

class UpdateUserRolesSerializer(serializers.Serializer):
    roles = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
    )

# class UpdateUserSerializer(serializers.Serializer):
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     email = serializers.EmailField()
#     is_active = serializers.BooleanField(required=False, default=True)
#     department = serializers.UUIDField()
#     roles = serializers.ListField(
#         child=serializers.UUIDField(),
#         required=True,
#         allow_empty=False,
#     )

#     def validate_email(self, value):
#         user_id = self.context.get("user_id")
#         if User.objects.filter(email=value).exclude(id=user_id).exists():
#             raise serializers.ValidationError("A user with that email already exists.")
#         return value

class UpdateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    department = serializers.UUIDField()
    roles = serializers.ListField(
        child=serializers.UUIDField(),
        required=True,
        allow_empty=False,
    )

    def validate_email(self, value):
        user_id = self.context.get("user_id")
        if User.objects.filter(email=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value
