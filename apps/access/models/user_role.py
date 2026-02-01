# access/models/user_role.py
from django.db import models


class UserRole(models.Model):
    user = models.ForeignKey("identity.User", on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey("access.Role", on_delete=models.CASCADE, related_name="role_users")

    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "role")
        db_table = "iam_user_role"
