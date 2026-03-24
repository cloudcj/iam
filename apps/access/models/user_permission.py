from django.db import models


class UserPermission(models.Model):

    SOURCE_ROLE   = "role"
    SOURCE_DIRECT = "direct"
    SOURCE_CHOICES = [
        (SOURCE_ROLE,   "Role"),
        (SOURCE_DIRECT, "Direct"),
    ]

    user = models.ForeignKey(
        "identity.User",
        on_delete=models.CASCADE,
        related_name="iam_user_permissions",
    )

    permission = models.ForeignKey(
        "access.Permission",
        on_delete=models.CASCADE,
        related_name="iam_user_permissions",
    )

    assigned_by = models.ForeignKey(
        "identity.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_permissions",
    )

    source = models.CharField(
        max_length=10,
        choices=SOURCE_CHOICES,
        default=SOURCE_ROLE,
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "permission")
        db_table = "iam_user_permission"
