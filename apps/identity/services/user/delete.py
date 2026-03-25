from django.core.exceptions import ValidationError, PermissionDenied
from django.db import transaction
from django.contrib.auth import get_user_model

from apps.common.constants import RoleCodes, HIDDEN_FROM_DEPARTMENT_ADMIN
from apps.common.helpers.authz.role_helpers import has_role

User = get_user_model()


@transaction.atomic
def delete_user(*, actor, target):
    if not target.is_active:
        raise ValidationError("User is already deactivated.")

    if actor.id == target.id:
        raise PermissionDenied("You cannot delete your own account.")

    is_superuser = actor.is_superuser
    is_platform_admin = has_role(actor, RoleCodes.PLATFORM_ADMIN)
    is_dept_admin = has_role(actor, RoleCodes.DEPT_ADMIN)

    if not is_superuser and not is_platform_admin and not is_dept_admin:
        raise PermissionDenied("You do not have permission to delete users.")

    if is_dept_admin:
        if target.user_roles.filter(role__code__in=HIDDEN_FROM_DEPARTMENT_ADMIN).exists():
            raise PermissionDenied("You cannot delete this user.")
        if actor.department_id != target.department_id:
            raise PermissionDenied("You cannot delete a user outside your department.")

    target.soft_delete()
