# from rest_framework import serializers
# from apps.identity.models import User

# MANAGEMENT_SYSTEMS = {"platform", "department"}


# class UserListSerializer(serializers.ModelSerializer):
#     department = serializers.SerializerMethodField()
#     management_role = serializers.SerializerMethodField()
#     system_roles = serializers.SerializerMethodField()

#     def get_department(self, obj):
#         if obj.department:
#             return {
#                 "id": str(obj.department.id),
#                 "code": obj.department.code,
#                 "name": obj.department.name,
#             }
#         return None

#     def _role_data(self, ur):
#         return {
#             "id": str(ur.role.id),
#             "code": ur.role.code,
#             "name": ur.role.name,
#             "system": ur.role.code.split(".")[0],
#         }

#     def get_management_role(self, obj):
#         for ur in obj.user_roles.select_related("role").all():
#             if ur.role.code.split(".")[0] in MANAGEMENT_SYSTEMS:
#                 return self._role_data(ur)
#         return None

#     def get_system_roles(self, obj):
#         return [
#             self._role_data(ur)
#             for ur in obj.user_roles.select_related("role").all()
#             if ur.role.code.split(".")[0] not in MANAGEMENT_SYSTEMS
#         ]

#     class Meta:
#         model = User
#         fields = [
#             "id",
#             "username",
#             "email",
#             "first_name",
#             "last_name",
#             "is_active",
#             "department",
#             "management_role",
#             "system_roles",
#         ]
#         read_only_fields = fields


from rest_framework import serializers
from apps.identity.models import User

MANAGEMENT_SYSTEMS = {"platform", "department"}
META_SYSTEMS = {"iam"}


class UserListSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    management_role = serializers.SerializerMethodField()
    system_roles = serializers.SerializerMethodField()

    def get_department(self, obj):
        if obj.department:
            return {
                "id": str(obj.department.id),
                "code": obj.department.code,
                "name": obj.department.name,
            }
        return None

    def _role_data(self, ur):
        system = ur.role.code.split(".")[0]
        data = {
            "id": str(ur.role.id),
            "code": ur.role.code,
            "name": ur.role.name,
            "system": system,
        }
        if system in MANAGEMENT_SYSTEMS:
            grants = list(dict.fromkeys(
                rp.policy.system
                for rp in ur.role.role_policies.all()
                if rp.policy.system not in META_SYSTEMS
            ))
            data["grants_systems"] = grants
        return data

    def get_management_role(self, obj):
        for ur in obj.user_roles.all():
            if ur.role.code.split(".")[0] in MANAGEMENT_SYSTEMS:
                return self._role_data(ur)
        return None

    def get_system_roles(self, obj):
        return [
            self._role_data(ur)
            for ur in obj.user_roles.all()
            if ur.role.code.split(".")[0] not in MANAGEMENT_SYSTEMS
        ]

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "department",
            "management_role",
            "system_roles",
        ]
        read_only_fields = fields
