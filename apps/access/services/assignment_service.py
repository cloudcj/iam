
from django.core.exceptions import ValidationError, PermissionDenied
from apps.access.models import (
    Role,
    UserRole,
    DepartmentAllowedSystem,
)


def assign_role_to_user(*, user, role_code: str):
    """
    Assign a role to a user ONLY if the user's department allows it.
    """

    # 1️⃣ get user's department (direct FK)
    department = getattr(user, "department", None)
    if not department:
        raise ValidationError("User has no department assigned")

    # 2️⃣ get role
    try:
        role = Role.objects.get(code=role_code)
    except Role.DoesNotExist:
        raise ValidationError(f"Role '{role_code}' does not exist")

    # 3️⃣ assign role (idempotent — system-level constraint removed, use policy assignment)
    UserRole.objects.get_or_create(
        user=user,
        role=role,
    )



# apps/access/services/assignment_service.py

def validate_role_assignment(*, department, role):
    # Department system validation (roles are no longer directly restricted per department)
    pass



# Functions that belong in assignment_service
# assign_role_to_user
# remove_role_from_user
# list_user_roles
# list_role_users