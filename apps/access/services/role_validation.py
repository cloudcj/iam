from rest_framework.exceptions import ValidationError

from apps.access.models import Role, DepartmentAllowedRole
from apps.department.models import UserDepartment
from apps.common.constants import GLOBAL_ROLES


def validate_role_assignment(*, user, role_code: str) -> Role:
    """
    Validate whether a role can be assigned to a user.
    Returns the Role if valid.
    Raises ValidationError if invalid.
    """

    # 1️⃣ Role must exist
    try:
        role = Role.objects.get(code=role_code)
    except Role.DoesNotExist:
        raise ValidationError(f"Role '{role_code}' does not exist")

    # 2️⃣ Global roles bypass department rules (by design)
    if role.code in GLOBAL_ROLES:
        return role

    # 3️⃣ User must have a department
    try:
        user_department = (
            UserDepartment.objects
            .select_related("department")
            .get(user=user)
        )
    except UserDepartment.DoesNotExist:
        raise ValidationError("User has no department assigned")

    # 4️⃣ Department-scoped role validation
    if not DepartmentAllowedRole.objects.filter(
        department=user_department.department,
        role=role,
    ).exists():
        raise ValidationError(
            f"Role '{role.code}' is not allowed in department "
            f"'{user_department.department.code}'"
        )

    return role




# from rest_framework.exceptions import ValidationError
# from apps.access.models import (
#     Role,
#     DepartmentAllowedRole
# )
# from apps.department.models import UserDepartment

# from apps.common.constants import GLOBAL_ROLES
# from seeder.seeder_data import DEPARTMENT_ALLOWED_ROLES

# def validate_role_assignment(*, user, role_code: str) -> Role:
#     """
#     Validate that a role:
#     - exists
#     - is allowed in the user's department
#     """

#     # 1️⃣ role must exist
#     try:
#         role = Role.objects.get(code=role_code)
#     except Role.DoesNotExist:
#         raise ValidationError(f"Role '{role_code}' does not exist")

#     # 2️⃣ user must have a department
#     try:
#         user_dept = UserDepartment.objects.select_related("department").get(user=user)
#     except UserDepartment.DoesNotExist:
#         raise ValidationError("User has no department assigned")

#     department_code = user_dept.department.code

#     # 3️⃣ department → role rule
#     allowed_roles = DEPARTMENT_ALLOWED_ROLES.get(department_code, [])

#     if role_code not in allowed_roles:
#         raise ValidationError(
#             f"Role '{role_code}' is not allowed in department '{department_code}'"
#         )

#     return role
