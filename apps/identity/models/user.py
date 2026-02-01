import uuid
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from ..managers import UserManager, ActiveUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Universal identity User
    - Identity only
    - No provisioning logic
    - No RBAC logic
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # ---- Identity ----
    username = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
    )

    email = models.EmailField(
        null=True,
        blank=True,
        db_index=True,
    )

    # ---- Account state ----
    is_active = models.BooleanField(default=True, db_index=True)
    is_staff = models.BooleanField(default=False)

    deleted_at = models.DateTimeField(null=True, blank=True)

    # ---- Audit ----
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ---- Django auth config ----
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    # ---- Managers ----
    objects = UserManager()
    active = ActiveUserManager()


    # ---- Lifecycle helpers (ALLOWED) ----
    def soft_delete(self):
        if not self.is_active:
            return
        self.is_active = False
        self.deleted_at = now()
        self.save(update_fields=["is_active", "deleted_at"])


    def restore(self):
        self.is_active = True
        self.deleted_at = None
        self.save(update_fields=["is_active", "deleted_at"])

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'iam_user'
