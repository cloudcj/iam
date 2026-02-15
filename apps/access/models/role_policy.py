# apps/access/models/role_policy.py
from django.db import models


class RolePolicy(models.Model):
    """
    Assigns policies to roles.
    Roles select policies, not raw permissions.
    """

    role = models.ForeignKey(
        "access.Role",
        on_delete=models.CASCADE,
        related_name="role_policies",
    )

    policy = models.ForeignKey(
        "access.Policy",
        on_delete=models.CASCADE,
        related_name="policy_roles",
    )

    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ("role", "policy")
        db_table = "iam_role_policy"
