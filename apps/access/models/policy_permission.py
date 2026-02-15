# apps/access/models/policy_permission.py
from django.db import models


class PolicyPermission(models.Model):
    """
    Expands a policy into concrete permissions.
    Example:
      inventory.az.read_update
        → inventory.az.read
        → inventory.az.update
    """

    policy = models.ForeignKey(
        "access.Policy",
        on_delete=models.CASCADE,
        related_name="policy_permissions",
    )

    permission = models.ForeignKey(
        "access.Permission",
        on_delete=models.CASCADE,
        related_name="permission_policies",
    )

    class Meta:
        unique_together = ("policy", "permission")
        db_table = "iam_policy_permission"
        # indexes = [
        #     models.Index(fields=["policy"]),
        #     models.Index(fields=["permission"]),
        # ]

