from django.db import transaction
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.common.constants import HIDDEN_FROM_IAM_ADMIN

from seeder.constants import RoleCodes
from apps.common.helpers.authz.role_helpers import has_role
from apps.identity.models import User


@transaction.atomic
def update_user_basic_info(
    *,
    actor: AbstractBaseUser,
    target: AbstractBaseUser,
    data: dict,
):
    # ❌ no self-update
    if actor.id == target.id:
        raise PermissionDenied("You cannot update your own account")

    # who can update?
    if not (
        has_role(actor, RoleCodes.SUPER_ADMIN)
        or has_role(actor, RoleCodes.IAM_ADMIN)
    ):
        raise PermissionDenied("Not allowed to update users")

    # IAM_ADMIN restrictions
    if has_role(actor, RoleCodes.IAM_ADMIN) and not has_role(actor, RoleCodes.SUPER_ADMIN):

        # ❌ cannot touch admin users
        if target.user_roles.filter(
            role__code__in=HIDDEN_FROM_IAM_ADMIN
        ).exists():
            raise PermissionDenied("Cannot modify admin users")

        # ❌ must be same department
        actor_dept = actor.user_department.first()
        target_dept = target.user_department.first()

        if not actor_dept or not target_dept:
            raise PermissionDenied("Department mismatch")

        if actor_dept.department_id != target_dept.department_id:
            raise PermissionDenied("Cannot modify users in another department")

    # 🔎 validate username uniqueness
    new_username = data.get("username")
    if new_username and User.objects.exclude(id=target.id).filter(username=new_username).exists():
        raise ValidationError("Username already exists")

    # 📝 apply updates (explicit)
    if "username" in data:
        target.username = data["username"]

    if "email" in data:
        target.email = data["email"] or ""

    target.save(update_fields=["username", "email"])

    return target
