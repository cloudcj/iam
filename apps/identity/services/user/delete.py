# identity/services/user_delete.py

from django.core.exceptions import ValidationError
from django.db import transaction
from apps.identity.models import User


@transaction.atomic
def soft_delete_user(*, user: User):
    if not user.is_active:
        raise ValidationError("User is already deactivated")

    user.soft_delete()
    return True
