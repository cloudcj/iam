import uuid
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from ..managers import UserManager, ActiveUserManager


# class User(AbstractBaseUser, PermissionsMixin):
#     """
#     Universal identity User
#     - Identity only
#     - No provisioning logic
#     - No RBAC logic
#     """

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

#     # ---- Identity ----
#     username = models.CharField(
#         max_length=150,
#         unique=True,
#         db_index=True,
#     )

#     email = models.EmailField(
#         null=True,
#         blank=True,
#         db_index=True,
#     )

#     # ---- Account state ----
#     is_active = models.BooleanField(default=True, db_index=True)
#     is_staff = models.BooleanField(default=False)

#     deleted_at = models.DateTimeField(null=True, blank=True)

#     # ---- Audit ----
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     # ---- Django auth config ----
#     USERNAME_FIELD = "username"
#     REQUIRED_FIELDS = []

#     # ---- Managers ----
#     objects = UserManager()
#     active = ActiveUserManager()
# apps/identity/models/user.py

import uuid

from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from ..managers import UserManager, ActiveUserManager

from apps.authz.service.authorization_service import AuthorizationService


class User(AbstractBaseUser, PermissionsMixin):
    """
    Universal IAM User
    - Identity only
    - Authorization delegated to IAM tables
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # ---- Identity ----
    username = models.CharField(max_length=150, unique=True, db_index=True)
    email = models.EmailField(null=True, blank=True, db_index=True)

    # ---- Org ownership (REQUIRED) ----
    department = models.ForeignKey(
        "department.Department",
        on_delete=models.PROTECT,
        related_name="users",
    )

    # ---- Account state ----
    is_active = models.BooleanField(default=True, db_index=True)
    is_staff = models.BooleanField(default=False)

    deactivated_at = models.DateTimeField(null=True, blank=True)

    # ---- Audit ----
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ---- Django auth config ----
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS: list[str] = []

    # ---- Managers ----
    objects = UserManager()
    active = ActiveUserManager()

    class Meta:
        db_table = "iam_user"

    def __str__(self) -> str:
        return self.username

    # ---- Lifecycle helpers ----
    def soft_delete(self):
        if not self.is_active:
            return
        self.is_active = False
        self.deactivated_at = now()
        self.save(update_fields=["is_active", "deactivated_at"])

    def restore(self):
        self.is_active = True
        self.deactivated_at = None
        self.save(update_fields=["is_active", "deactivated_at"])


    # ---- Authorization ----

   # iam/models/user.py
    def has_permission(self, permission_code: str) -> bool:
        return AuthorizationService.has_permission(self, permission_code)





    # def has_permission(self, permission_code: str) -> bool:
    #     """
    #     Returns True if the user has the given permission
    #     via roles or directly assigned policies.
    #     """

    #     # 🔐 Superadmin bypass (by design)
    #     if self.is_superuser:
    #         return True

    #     # 1️⃣ Permissions via roles → policies
    #     via_roles = Permission.objects.filter(
    #         policy_permissions__policy__policy_roles__role__user_roles__user=self,
    #         code=permission_code,
    #     ).exists()

    #     if via_roles:
    #         return True

    #     # 2️⃣ Permissions via direct user policies
    #     via_user_policies = Permission.objects.filter(
    #         policy_permissions__policy__policy_users__user=self,
    #         code=permission_code,
    #     ).exists()

    #     return via_user_policies
