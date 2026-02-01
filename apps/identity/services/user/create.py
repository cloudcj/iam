from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError

from apps.identity.models import User
from apps.department.models import Department,UserDepartment
from apps.access.models import Role,DepartmentAllowedRole
from apps.access.services import assign_role_to_user

@transaction.atomic
def create_user(
    *,
    username,
    password,
    department_code,
    role_codes,
    email=None,
):
    if not role_codes:
        raise ValidationError("At least one role is required")

    if User.objects.filter(username=username).exists():
        raise ValidationError("Username already exists")

    # Validate department
    try:
        department = Department.objects.get(code=department_code)
    except Department.DoesNotExist:
        raise ValidationError("Invalid department")

    # Validate allowed roles
    allowed_roles = set(
        DepartmentAllowedRole.objects.filter(
            department=department
        ).values_list("role__code", flat=True)
    )

    for role_code in role_codes:
        if role_code not in allowed_roles:
            raise ValidationError(
                f"Role {role_code} is not allowed for department {department.code}"
            )

    roles = []
    for role_code in role_codes:
        try:
            roles.append(Role.objects.get(code=role_code))
        except Role.DoesNotExist:
            raise ValidationError(f"Invalid role: {role_code}")

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
    )

    UserDepartment.objects.create(
        user=user,
        department=department,
    )

    for role in roles:
        assign_role_to_user(user=user, role_code=role.code)

    return user