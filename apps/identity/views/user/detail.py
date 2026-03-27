from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from apps.identity.models import User
from apps.access.models import UserPermission
from apps.access.models.policy import Policy
from apps.authz.permissions import HasPermission
from apps.authz.services.authorization_service import AuthorizationService
from apps.common.constants.permission_codes import IAMPermissions


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = IAMPermissions.USER_READ

    def get(self, request, user_id):
        target = get_object_or_404(User, id=user_id)

        # Current roles
        role_ids = list(
            target.user_roles.values_list("role_id", flat=True)
        )

        # ALL resolved permission codes (from roles + direct)
        all_permission_codes = set(
            AuthorizationService.get_user_permission_codes(target)
        )

        # Current source=direct permission IDs
        direct_perm_ids = set(
            UserPermission.objects
            .filter(user=target, source=UserPermission.SOURCE_DIRECT)
            .values_list("permission_id", flat=True)
        )

        # Individual permissions = source=direct that aren't covered by any policy
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
            "department": str(target.department_id) if target.department_id else None,
            "roles": [str(r) for r in role_ids],
            "permission_codes": list(all_permission_codes),
            "extra_permission_ids": extra_permission_ids,
        })
