from rest_framework.exceptions import ValidationError

from apps.access.models import Role, DepartmentAllowedRole
from apps.common.constants import GLOBAL_ROLES


def validate_role_assignment(*, user, role_code: str) -> Role:
    """
    Validate whether a role can be assigned to a user.
    Returns the Role if valid.
    """

    # 1️⃣ Role must exist
    try:
        role = Role.objects.get(code=role_code)
    except Role.DoesNotExist:
        raise ValidationError(f"Role '{role_code}' does not exist")

    # 2️⃣ Global roles bypass department rules
    if role.code in GLOBAL_ROLES:
        return role

    # 3️⃣ User must have a department (FK)
    department = getattr(user, "department", None)
    if not department:
        raise ValidationError("User has no department assigned")

    # 4️⃣ Department-scoped role validation
    if not DepartmentAllowedRole.objects.filter(
        department=department,
        role=role,
    ).exists():
        raise ValidationError(
            f"Role '{role.code}' is not allowed in department '{department.code}'"
        )

    return role
