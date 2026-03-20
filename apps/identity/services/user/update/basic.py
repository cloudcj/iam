# from django.db import transaction
# from django.core.exceptions import ValidationError

# from apps.identity.models import User


# @transaction.atomic
# def update_user_basic(*, user_id, email=None, is_active=None):
#     try:
#         user = User.objects.select_for_update().get(id=user_id)
#     except User.DoesNotExist:
#         raise ValidationError("User not found")

#     if email is not None:
#         user.email = email

#     if is_active is not None:
#         user.is_active = is_active

#     user.save()
#     return user


from django.db import transaction
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.common.constants import RoleCodes, HIDDEN_FROM_IAM_ADMIN
from apps.common.helpers.authz.role_helpers import has_role
from apps.identity.models import User


@transaction.atomic
def update_user_basic(
    *,
    actor: AbstractBaseUser,
    target: AbstractBaseUser,
    data: dict,
):
    # ❌ no self-update
    if actor.id == target.id:
        raise PermissionDenied("You cannot update your own account")

    # 🔐 who can update?
    if not (actor.is_superuser or has_role(actor, RoleCodes.IAM_ADMIN)):
        raise PermissionDenied("Not allowed to update users")

    # IAM_ADMIN restrictions
    if has_role(actor, RoleCodes.IAM_ADMIN) and not actor.is_superuser:

        # ❌ cannot touch admin users
        if target.user_roles.filter(role__code__in=HIDDEN_FROM_IAM_ADMIN).exists():
            raise PermissionDenied("Cannot modify admin users")

        # ❌ must be same department
        if not actor.department or not target.department:
            raise PermissionDenied("Department mismatch")

        if actor.department_id != target.department_id:
            raise PermissionDenied("Cannot modify users in another department")

    # 🔎 validate username uniqueness
    new_username = data.get("username")
    if new_username and User.objects.exclude(id=target.id).filter(username=new_username).exists():
        raise ValidationError("Username already exists")

    # 📝 apply updates
    if "username" in data:
        target.username = data["username"]

    if "email" in data:
        target.email = data["email"] or ""

    target.save(update_fields=["username", "email"])

    return target