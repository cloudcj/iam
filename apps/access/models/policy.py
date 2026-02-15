# apps/access/models/policy.py
import uuid
from django.db import models


class Policy(models.Model):
    """
    High-level access intent selected by admins / UI.
    Example: inventory.az.read_update
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    code = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Stable policy identifier (DO NOT CHANGE)",
    )

    label = models.CharField(
        max_length=100,
        help_text="Human-readable label (e.g. AZ – Read & Update)",
    )

    system = models.CharField(
        max_length=50,
        help_text="Owning service (inventory, iam, monitoring)",
    )

    resource = models.CharField(
        max_length=50,
        help_text="Resource name (az, device, user, etc.)",
    )

    description = models.TextField(blank=True)


    def __str__(self):
        return self.code

    class Meta:
        db_table = "iam_policy"
