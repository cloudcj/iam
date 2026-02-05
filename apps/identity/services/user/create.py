from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError

from django.db import transaction
from django.contrib.auth import get_user_model

from apps.department.models import Department, UserDepartment
from seeder.constants import RoleCodes
from apps.access.services.role_validation import validate_role_assignment
from apps.access.services.role_assignment import assign_role_to_user

from apps.common.helpers.authz.role_helpers import has_role 

User = get_user_model()


# def has_role(user, role_code: str) -> bool:
#     return user.user_roles.filter(role__code=role_code).exists()


@transaction.atomic
def create_user(
    *,
    actor,
    username: str,
    password: str,
    department_code: str,
    role_codes: list[str],
    email: str | None = None,
):
    # 🔐 who can create users
    if not (
        has_role(actor, RoleCodes.SUPER_ADMIN)
        or has_role(actor, RoleCodes.IAM_ADMIN)
    ):
        raise PermissionDenied("Not allowed to create users")

    if not role_codes:
        raise ValidationError("At least one role is required")

    if User.objects.filter(username=username).exists():
        raise ValidationError("Username already exists")

    # 1️⃣ resolve department
    try:
        department = Department.objects.get(code=department_code)
    except Department.DoesNotExist:
        raise ValidationError("Invalid department")

    # 2️⃣ IAM_ADMIN scope restriction
    if has_role(actor, RoleCodes.IAM_ADMIN) and not has_role(actor, RoleCodes.SUPER_ADMIN):
        actor_dept = actor.user_department.first()
        if not actor_dept or actor_dept.department_id != department.id:
            raise PermissionDenied(
                "IAM admin cannot create users in another department"
            )

    # 3️⃣ prevent SUPER_ADMIN escalation
    if (
        RoleCodes.SUPER_ADMIN in role_codes
        and not has_role(actor, RoleCodes.SUPER_ADMIN)
    ):
        raise PermissionDenied("Cannot assign SUPER_ADMIN role")

    # 4️⃣ create user
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email or "",
        is_active=True,
    )

    # 5️⃣ assign department
    UserDepartment.objects.create(
        user=user,
        department=department,
    )

    # 6️⃣ validate + assign roles
    for role_code in role_codes:
        role = validate_role_assignment(
            user=user,
            role_code=role_code,
        )
        assign_role_to_user(
            user=user,
            role=role,
        )

    return user



# from django.core.exceptions import ValidationError
# from django.db import transaction, IntegrityError

# from apps.identity.models import User
# from apps.department.models import Department,UserDepartment
# from apps.access.models import Role,DepartmentAllowedRole
# from apps.access.services import assign_role_to_user

# @transaction.atomic
# def create_user(
#     *,
#     username,
#     password,
#     department_code,
#     role_codes,
#     email=None,
# ):
#     if not role_codes:
#         raise ValidationError("At least one role is required")

#     if User.objects.filter(username=username).exists():
#         raise ValidationError("Username already exists")

#     # Validate department
#     try:
#         department = Department.objects.get(code=department_code)
#     except Department.DoesNotExist:
#         raise ValidationError("Invalid department")

#     # Validate allowed roles
#     allowed_roles = set(
#         DepartmentAllowedRole.objects.filter(
#             department=department
#         ).values_list("role__code", flat=True)
#     )

#     for role_code in role_codes:
#         if role_code not in allowed_roles:
#             raise ValidationError(
#                 f"Role {role_code} is not allowed for department {department.code}"
#             )

#     roles = []
#     for role_code in role_codes:
#         try:
#             roles.append(Role.objects.get(code=role_code))
#         except Role.DoesNotExist:
#             raise ValidationError(f"Invalid role: {role_code}")

#     user = User.objects.create_user(
#         username=username,
#         password=password,
#         email=email,
#     )

#     UserDepartment.objects.create(
#         user=user,
#         department=department,
#     )

#     for role in roles:
#         assign_role_to_user(user=user, role_code=role.code)

#     return user