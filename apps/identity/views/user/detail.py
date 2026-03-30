# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django.shortcuts import get_object_or_404

# from apps.identity.models import User
# from apps.access.models import UserPermission
# from apps.access.models.policy import Policy
# from apps.authz.permissions import HasPermission
# from apps.authz.services.authorization_service import AuthorizationService
# from apps.common.constants.permission_codes import IAMPermissions

# MANAGEMENT_SYSTEMS = {"platform", "department"}


# class UserDetailView(APIView):
#     permission_classes = [IsAuthenticated, HasPermission]
#     required_permission = IAMPermissions.USER_READ

#     def get(self, request, user_id):
#         target = get_object_or_404(User, id=user_id)

#         user_roles = list(target.user_roles.select_related("role").all())

#         def role_data(ur):
#             return {
#                 "id": str(ur.role.id),
#                 "code": ur.role.code,
#                 "name": ur.role.name,
#                 "system": ur.role.code.split(".")[0],
#             }

#         management_role = next(
#             (role_data(ur) for ur in user_roles if ur.role.code.split(".")[0] in MANAGEMENT_SYSTEMS),
#             None
#         )
#         system_roles = [
#             role_data(ur) for ur in user_roles
#             if ur.role.code.split(".")[0] not in MANAGEMENT_SYSTEMS
#         ]

#         # ALL resolved permission codes (from roles + direct)
#         all_permission_codes = set(
#             AuthorizationService.get_user_permission_codes(target)
#         )

#         # Current source=direct permission IDs
#         direct_perm_ids = set(
#             UserPermission.objects
#             .filter(user=target, source=UserPermission.SOURCE_DIRECT)
#             .values_list("permission_id", flat=True)
#         )

#         # Individual permissions = source=direct that aren't covered by any policy
#         covered_perm_ids = set()
#         policies = Policy.objects.prefetch_related("policy_permissions").all()
#         for policy in policies:
#             policy_perm_ids = set(
#                 policy.policy_permissions.values_list("permission_id", flat=True)
#             )
#             if policy_perm_ids and policy_perm_ids.issubset(direct_perm_ids):
#                 covered_perm_ids.update(policy_perm_ids)

#         extra_permission_ids = [
#             str(pid) for pid in direct_perm_ids
#             if pid not in covered_perm_ids
#         ]

#         return Response({
#             "id": str(target.id),
#             "username": target.username,
#             "first_name": target.first_name,
#             "last_name": target.last_name,
#             "email": target.email,
#             "is_active": target.is_active,
#             "department": {
#                 "id": str(target.department.id),
#                 "code": target.department.code,
#                 "name": target.department.name,
#             } if target.department else None,
#             "management_role": management_role,
#             "system_roles": system_roles,
#             "permission_codes": list(all_permission_codes),
#             "extra_permission_ids": extra_permission_ids,
#         })


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from apps.identity.models import User
from apps.access.models import UserPermission
from apps.access.models.policy import Policy
from apps.access.models.permission import Permission
from apps.authz.permissions import HasPermission
from apps.authz.services.authorization_service import AuthorizationService
from apps.common.constants.permission_codes import IAMPermissions

MANAGEMENT_SYSTEMS = {"platform", "department"}
META_SYSTEMS = {"iam"}


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = IAMPermissions.USER_READ

    def get(self, request, user_id):
        target = get_object_or_404(
            User.objects.select_related("department")
                        .prefetch_related(
                            "user_roles__role",
                            "user_roles__role__role_policies__policy",
                        ),
            id=user_id,
        )

        def role_data(ur):
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

        user_roles = list(target.user_roles.all())

        management_role = next(
            (role_data(ur) for ur in user_roles if ur.role.code.split(".")[0] in MANAGEMENT_SYSTEMS),
            None
        )
        system_roles = [
            role_data(ur) for ur in user_roles
            if ur.role.code.split(".")[0] not in MANAGEMENT_SYSTEMS
        ]

        all_permission_codes = set(
            AuthorizationService.get_user_permission_codes(target)
        )

        all_permission_ids = list(
            Permission.objects
            .filter(code__in=all_permission_codes)
            .values_list("id", flat=True)
        )

        direct_perm_ids = set(
            UserPermission.objects
            .filter(user=target, source=UserPermission.SOURCE_DIRECT)
            .values_list("permission_id", flat=True)
        )

        covered_perm_ids = set()
        policies = Policy.objects.prefetch_related("policy_permissions").all()
        for policy in policies:
            policy_perm_ids = set(
                policy.policy_permissions.values_list("permission_id", flat=True)
            )
            if policy_perm_ids and policy_perm_ids.issubset(direct_perm_ids):
                covered_perm_ids.update(policy_perm_ids)

        extra_permission_ids = [
            str(pid) for pid in direct_perm_ids
            if pid not in covered_perm_ids
        ]

        return Response({
            "id": str(target.id),
            "username": target.username,
            "first_name": target.first_name,
            "last_name": target.last_name,
            "email": target.email,
            "is_active": target.is_active,
            "department": {
                "id": str(target.department.id),
                "code": target.department.code,
                "name": target.department.name,
            } if target.department else None,
            "management_role": management_role,
            "system_roles": system_roles,
            "permission_codes": list(all_permission_codes),
            "permission_ids": [str(pid) for pid in all_permission_ids],
            "extra_permission_ids": extra_permission_ids,
        })
