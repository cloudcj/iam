# identity/serializers/user.py

from rest_framework import serializers
from apps.identity.models import User

# class UserListSerializer(serializers.ModelSerializer):
#     department = serializers.CharField(
#         source="user_department.department.name",
#         read_only=True,
#     )

#     roles = serializers.SlugRelatedField(
#         many=True,
#         read_only=True,
#         slug_field="code",
#         source="user_roles.role",
#     )


#     class Meta:
#         model = User
#         fields = [
#             "id",
#             "username",
#             "email",
#             "is_active",
#             "department",
#             "roles",
#         ]
#         read_only_fields = fields

class UserListSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    def get_department(self, obj):
        link = obj.user_department.first()
        return link.department.code if link else None

    def get_roles(self, obj):
        return [ur.role.code for ur in obj.user_roles.all()]

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "is_active",
            "department",
            "roles",
        ]
        read_only_fields = fields
