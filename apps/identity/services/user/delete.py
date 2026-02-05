# # identity/services/user_delete.py

# from django.core.exceptions import ValidationError
# from django.db import transaction
# from apps.identity.models import User


# @transaction.atomic
# def soft_delete_user(*, user: User):
#     if not user.is_active:
#         raise ValidationError("User is already deactivated")

#     user.soft_delete()
#     return True


from django.core.exceptions import ValidationError, PermissionDenied
from django.db import transaction
from django.contrib.auth import get_user_model

from seeder.constants import RoleCodes
from apps.common.helpers.authz.role_helpers import has_role
from django.contrib.auth.models import AbstractBaseUser

from apps.common.constants import HIDDEN_FROM_IAM_ADMIN


@transaction.atomic
def soft_delete_user(*, actor: AbstractBaseUser, target: AbstractBaseUser):
    # already inactive
    if not target.is_active:
        raise ValidationError("User is already deactivated")

    # no self-delete
    if actor.id == target.id:
        raise PermissionDenied("You cannot delete your own account")

    # who can delete?
    if not (
        has_role(actor, RoleCodes.SUPER_ADMIN)
        or has_role(actor, RoleCodes.IAM_ADMIN)
    ):
        raise PermissionDenied("Not allowed to delete users")

    # IAM_ADMIN restrictions
    if has_role(actor, RoleCodes.IAM_ADMIN) and not has_role(actor, RoleCodes.SUPER_ADMIN):

        # ❌ cannot delete hidden / higher / peer roles
        if target.user_roles.filter(
            role__code__in=HIDDEN_FROM_IAM_ADMIN
        ).exists():
            raise PermissionDenied("Cannot delete admin users")

        actor_dept = actor.user_department.first()
        target_dept = target.user_department.first()

        if not actor_dept or not target_dept:
            raise PermissionDenied("Department mismatch")

        if actor_dept.department_id != target_dept.department_id:
            raise PermissionDenied("Cannot delete user in another department")

    # soft delete (explicit, auditable)
    target.is_active = False
    target.save(update_fields=["is_active"])

    return True