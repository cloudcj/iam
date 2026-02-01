from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    Default user manager.

    Used by:
    - Django internals
    - admin
    - migrations
    - management commands

    IMPORTANT:
    - MUST NOT filter users
    """

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")

        username = self.model.normalize_username(username)

        user = self.model(
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(username, password, **extra_fields)


class ActiveUserManager(BaseUserManager):
    """
    Explicit manager for *active* users only.

    Use this ONLY for:
    - authentication
    - token issuance
    - login-related flows

    NEVER use as default manager.
    """

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                is_active=True,
                deleted_at__isnull=True,
            )
        )
