from django.db import models


class AccessLog(models.Model):

    # Actor (from JWT — null if unauthenticated)
    user_id    = models.CharField(max_length=50, null=True, blank=True)
    username   = models.CharField(max_length=150, null=True, blank=True)
    department = models.CharField(max_length=150, null=True, blank=True)

    # Request info
    method      = models.CharField(max_length=10)
    path        = models.CharField(max_length=255)
    status_code = models.IntegerField()
    ip_address  = models.GenericIPAddressField(null=True, blank=True)
    browser     = models.CharField(max_length=200, null=True, blank=True)
    os_device   = models.CharField(max_length=200, null=True, blank=True)

    timestamp   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "logs_access_log"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["user_id"], name="idx_accesslog_user"),
            models.Index(fields=["status_code", "timestamp"], name="idx_accesslog_status_ts"),
        ]
