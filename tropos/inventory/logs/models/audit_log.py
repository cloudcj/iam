from django.db import models


class AuditLog(models.Model):

    ACTION_CREATE = "create"
    ACTION_UPDATE = "update"
    ACTION_DELETE = "delete"
    ACTION_CHOICES = [
        (ACTION_CREATE, "Create"),
        (ACTION_UPDATE, "Update"),
        (ACTION_DELETE, "Delete"),
    ]

    # Actor (from JWT)
    user_id    = models.CharField(max_length=50, null=True, blank=True)
    username   = models.CharField(max_length=150, null=True, blank=True)
    department = models.CharField(max_length=150, null=True, blank=True)

    # What happened
    action     = models.CharField(max_length=20, choices=ACTION_CHOICES)
    target     = models.CharField(max_length=200)
    target_id  = models.CharField(max_length=50, null=True, blank=True)
    status     = models.CharField(max_length=20, default="success")

    # Request info
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    browser    = models.CharField(max_length=200, null=True, blank=True)
    os_device  = models.CharField(max_length=200, null=True, blank=True)

    # Details
    detail     = models.JSONField(null=True, blank=True)

    timestamp  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "logs_audit_log"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["user_id"], name="idx_auditlog_user"),
            models.Index(fields=["action", "timestamp"], name="idx_auditlog_action_ts"),
        ]
