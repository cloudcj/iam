
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError

from apps.access.models import (
    Role,
    UserRole,
)
from apps.department.models import UserDepartment


from django.contrib.auth.models import AbstractBaseUser


def assign_role_to_user(*, user: AbstractBaseUser, role: Role):
    """
    Assign a role to a user.
    Assumes validation has already happened.
    """
    UserRole.objects.get_or_create(
        user=user,
        role=role,
    )