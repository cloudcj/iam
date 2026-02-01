
from django.core.exceptions import ValidationError, PermissionDenied
from apps.access.models import (
    Role,
    UserRole,
    DepartmentAllowedRole,
)
from apps.department.models import UserDepartment


def assign_role_to_user(*, user, role_code: str):
    """
    Assign a role to a user ONLY if the user's department allows it.
    """

    # 1️⃣ get user's department
    try:
        user_department = (
            UserDepartment.objects
            .select_related("department")
            .get(user=user)
        )
    except UserDepartment.DoesNotExist:
        raise ValidationError("User has no department assigned")

    department = user_department.department

    # 2️⃣ get role
    try:
        role = Role.objects.get(code=role_code)
    except Role.DoesNotExist:
        raise ValidationError(f"Role '{role_code}' does not exist")

    # 3️⃣ validate department → role
    if not DepartmentAllowedRole.objects.filter(
        department=department,
        role=role,
    ).exists():
        raise ValidationError(
            f"Role '{role.code}' is not allowed in department '{department.code}'"
        )

    # 4️⃣ assign role (idempotent)
    UserRole.objects.get_or_create(
        user=user,
        role=role,
    )



# apps/access/services/assignment_service.py

def validate_role_assignment(*, department, role):
    if not DepartmentAllowedRole.objects.filter(
        department=department,
        role=role,
    ).exists():
        raise PermissionDenied("Role not allowed for this department")



# Functions that belong in assignment_service
# assign_role_to_user
# remove_role_from_user
# list_user_roles
# list_role_users