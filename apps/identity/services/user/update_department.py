from django.db import transaction
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.exceptions import PermissionDenied, ValidationError

from seeder.constants import RoleCodes
from apps.common.helpers.authz.role_helpers import has_role
from apps.department.models import Department, UserDepartment


@transaction.atomic
def update_user_department(
    *,
    actor: AbstractBaseUser,
    target: AbstractBaseUser,
    department_code: str,
):
    # ❌ no self-update
    if actor.id == target.id:
        raise PermissionDenied("You cannot update your own department")

    # 🔐 SUPER_ADMIN only
    if not has_role(actor, RoleCodes.SUPER_ADMIN):
        raise PermissionDenied("Only SUPER_ADMIN can change department")

    # 🔎 resolve department
    try:
        department = Department.objects.get(code=department_code)
    except Department.DoesNotExist:
        raise ValidationError("Invalid department")

    # 🔁 upsert department link
    UserDepartment.objects.update_or_create(
        user=target,
        defaults={"department": department},
    )

    return True
