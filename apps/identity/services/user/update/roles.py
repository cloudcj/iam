
# from django.db import transaction
# from django.core.exceptions import ValidationError

# from apps.identity.models import User
# from apps.access.models import Role,UserRole

# @transaction.atomic
# def update_user_role(*, user: User, role_codes: list[str]):
#     if not role_codes:
#         raise ValidationError("User must have at least one role")

#     department = user.department

#     roles = list(Role.objects.filter(code__in=role_codes))
#     if len(roles) != len(set(role_codes)):
#         raise ValidationError("One or more roles are invalid")

#     # Validate roles belong to dept's allowed systems
#     allowed_systems = list(
#         department.allowed_system_entries.values_list("system", flat=True)
#     )
#     for role in roles:
#         role_system = role.code.split(".")[0]
#         if role_system not in allowed_systems:
#             raise ValidationError(
#                 f"Role '{role.code}' is not allowed in department '{department.code}'"
#             )

#     UserRole.objects.filter(user=user).delete()
#     UserRole.objects.bulk_create(
#         [UserRole(user=user, role=role) for role in roles]
#     )
#     return True
# # @transaction.atomic
# # def update_user_role(*, user: User, role_codes: list[str]):
# #     if not role_codes:
# #         raise ValidationError("User must have at least one role")

# #     # Ensure user has a department
# #     try:
# #         user_department = UserDepartment.objects.select_related("department").get(
# #             user=user
# #         )
# #     except UserDepartment.DoesNotExist:
# #         raise ValidationError("User has no department assigned")

# #     department = user_department.department

# #     # Fetch roles in one query
# #     roles = list(Role.objects.filter(code__in=role_codes))
# #     if len(roles) != len(set(role_codes)):
# #         raise ValidationError("One or more roles are invalid")

# #     # Allowed roles for department
# #     allowed_role_ids = set(
# #         DepartmentAllowedRole.objects.filter(
# #             department=department
# #         ).values_list("role_id", flat=True)
# #     )

# #     for role in roles:
# #         if role.id not in allowed_role_ids:
# #             raise ValidationError(
# #                 f"Role '{role.code}' is not allowed in department '{department.code}'"
# #             )

#     # Replace roles atomically
#     UserRole.objects.filter(user=user).delete()
#     UserRole.objects.bulk_create(
#         [UserRole(user=user, role=role) for role in roles]
#     )

#     return True




from django.db import transaction
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.common.constants import RoleCodes, HIDDEN_FROM_IAM_ADMIN
from apps.common.helpers.authz.role_helpers import has_role
from apps.access.models import Role, UserRole
from apps.access.services.roles.role_validation import validate_role_assignment


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
    if not (actor.is_superuser or has_role(actor, RoleCodes.IAM_ADMIN)):
        raise PermissionDenied("Not allowed to update user roles")

    # IAM_ADMIN restrictions
    if has_role(actor, RoleCodes.IAM_ADMIN) and not actor.is_superuser:

        # ❌ cannot modify admin users
        if target.user_roles.filter(role__code__in=HIDDEN_FROM_IAM_ADMIN).exists():
            raise PermissionDenied("Cannot modify admin users")

        # ❌ cannot assign admin/global roles
        if any(code in HIDDEN_FROM_IAM_ADMIN for code in role_codes):
            raise PermissionDenied("Cannot assign admin roles")

        # ❌ must be same department
        if not actor.department or not target.department:
            raise PermissionDenied("Department mismatch")

        if actor.department_id != target.department_id:
            raise PermissionDenied("Cannot modify users in another department")

    # 🔎 validate roles exist
    roles = []
    for role_code in role_codes:
        role = validate_role_assignment(user=target, role_code=role_code)
        roles.append(role)

    # 🔁 replace roles atomically
    UserRole.objects.filter(user=target).delete()
    UserRole.objects.bulk_create(
        [UserRole(user=target, role=role) for role in roles]
    )

    return True