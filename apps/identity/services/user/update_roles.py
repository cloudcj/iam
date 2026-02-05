from django.db import transaction
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.common.constants import HIDDEN_FROM_IAM_ADMIN

from seeder.constants import RoleCodes
from apps.common.helpers.authz.role_helpers import has_role
from apps.access.models import Role, UserRole
from apps.access.services import validate_role_assignment

@transaction.atomic
def update_user_roles(
    *,
    actor: AbstractBaseUser,
    target: AbstractBaseUser,
    role_codes: list[str],
):
    # ❌ no self-update
    if actor.id == target.id:
        raise PermissionDenied("You cannot modify your own roles")

    if not role_codes:
        raise ValidationError("At least one role is required")

    # 🔐 who can update roles?
    if not (
        has_role(actor, RoleCodes.SUPER_ADMIN)
        or has_role(actor, RoleCodes.IAM_ADMIN)
    ):
        raise PermissionDenied("Not allowed to update user roles")

    # IAM_ADMIN restrictions
    if has_role(actor, RoleCodes.IAM_ADMIN) and not has_role(actor, RoleCodes.SUPER_ADMIN):

        # ❌ cannot modify admin users
        if target.user_roles.filter(
            role__code__in=HIDDEN_FROM_IAM_ADMIN
        ).exists():
            raise PermissionDenied("Cannot modify admin users")

        # ❌ cannot assign admin roles
        if any(code in HIDDEN_FROM_IAM_ADMIN for code in role_codes):
            raise PermissionDenied("Cannot assign admin roles")

        # ❌ must be same department
        actor_dept = actor.user_department.first()
        target_dept = target.user_department.first()

        if not actor_dept or not target_dept:
            raise PermissionDenied("Department mismatch")

        if actor_dept.department_id != target_dept.department_id:
            raise PermissionDenied("Cannot modify users in another department")

    # 🔎 resolve & validate roles (department-safe)
    roles = []
    for role_code in role_codes:
        role = validate_role_assignment(
            user=target,
            role_code=role_code,
        )
        roles.append(role)

    # 🔁 replace roles atomically
    UserRole.objects.filter(user=target).delete()

    UserRole.objects.bulk_create(
        [UserRole(user=target, role=role) for role in roles]
    )

    return True
