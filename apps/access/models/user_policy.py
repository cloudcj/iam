from django.db import models


class UserPolicy(models.Model):
    user = models.ForeignKey(
        "identity.User",
        on_delete=models.CASCADE,
        related_name="user_policies",
    )

    policy = models.ForeignKey(
        "access.Policy",
        on_delete=models.CASCADE,
        related_name="policy_users",
    )

    assigned_by = models.ForeignKey(
        "identity.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_policies",
    )

    assigned_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ("user", "policy")
        db_table = "iam_user_policy"
