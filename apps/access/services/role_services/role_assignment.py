
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError

from apps.access.models import (
    Role,
    UserPolicy,
    Policy
)
from apps.department.models import UserDepartment


from django.contrib.auth.models import AbstractBaseUser


# def assign_role_to_user(*, user: AbstractBaseUser, role: Role):
#     """
#     Assign a role to a user.
#     Assumes validation has already happened.
#     """
#     UserRole.objects.get_or_create(
#         user=user,
#         role=role,
#     )

from django.db import transaction


# @transaction.atomic
# def assign_roles_to_user(user, role_codes: list[str]):

#     # 1️⃣ Fetch roles
#     roles = Role.objects.filter(code__in=role_codes)

#     if roles.count() != len(role_codes):
#         existing = set(roles.values_list("code", flat=True))
#         missing = set(role_codes) - existing
#         raise RuntimeError(f"Invalid roles: {missing}")

#     # 2️⃣ Validate department constraint
#     allowed_role_codes = set(
#         user.department.roles.values_list("code", flat=True)
#     )

#     if not set(role_codes).issubset(allowed_role_codes):
#         raise RuntimeError(
#             "One or more roles are not allowed for this department"
#         )

#     # 3️⃣ Expand roles → policies
#     policies = Policy.objects.filter(
#         policy_roles__role__in=roles
#     ).distinct()

#     # 4️⃣ Replace existing policies (authoritative state)
#     UserPolicy.objects.filter(user=user).delete()

#     # 5️⃣ Create new policy grants
#     UserPolicy.objects.bulk_create(
#         [
#             UserPolicy(user=user, policy=policy)
#             for policy in policies
#         ]
#     )


@transaction.atomic
def assign_roles_to_user(user, role_codes: list[str]):

    # 1️⃣ Fetch roles
    roles = Role.objects.filter(code__in=role_codes)

    if roles.count() != len(role_codes):
        existing = set(roles.values_list("code", flat=True))
        missing = set(role_codes) - existing
        raise RuntimeError(f"Invalid roles: {missing}")

    # 2️⃣ Validate department constraint
    allowed_role_codes = set(
        user.department.roles.values_list("code", flat=True)
    )

    if not set(role_codes).issubset(allowed_role_codes):
        raise RuntimeError(
            "One or more roles are not allowed for this department"
        )

    # 3️⃣ Expand roles → policies
    policies = Policy.objects.filter(
        policy_roles__role__in=roles
    ).distinct()

    # 4️⃣ Replace existing policies (authoritative state)
    UserPolicy.objects.filter(user=user).delete()

    # 5️⃣ Create new policy grants
    UserPolicy.objects.bulk_create(
        [
            UserPolicy(user=user, policy=policy)
            for policy in policies
        ]
    )
