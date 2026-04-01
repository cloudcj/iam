from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.conf import settings


class AuditLog(models.Model):

    class Action(models.TextChoices):
        # Auth
        AUTH_LOGIN         = "auth.login"
        AUTH_LOGIN_FAILED  = "auth.login_failed"
        AUTH_LOGOUT        = "auth.logout"
        AUTH_TOKEN_REFRESH = "auth.token_refresh"
        AUTH_ACCOUNT_LOCKED = "auth.account_locked"

        # User management
        USER_CREATE         = "user.create"
        USER_UPDATE         = "user.update"
        USER_DELETE         = "user.delete"
        USER_RESET_PASSWORD = "user.reset_password"
        USER_CHANGE_PASSWORD = "user.change_password"

        # Department
        DEPT_CREATE = "department.create"
        DEPT_UPDATE = "department.update"
        DEPT_DELETE = "department.delete"

    class Status(models.TextChoices):
        SUCCESS = "success"
        FAILURE = "failure"

    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor      = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,        # null = anonymous (e.g. failed login)
        blank=True,
        on_delete=models.SET_NULL,
        related_name="audit_logs",
    )
    action     = models.CharField(max_length=50, choices=Action.choices, db_index=True)
    target_id  = models.UUIDField(null=True, blank=True)        # affected object's UUID
    target_type = models.CharField(max_length=50, blank=True)   # "user", "department"
    status     = models.CharField(max_length=10, choices=Status.choices, default=Status.SUCCESS)
    detail     = models.JSONField(default=dict, blank=True)     # extra context
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp  = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "iam_audit_log"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.timestamp} | {self.actor} | {self.action} | {self.status}"
