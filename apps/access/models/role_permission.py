# access/models/role_permission.py
from django.db import models


class RolePermission(models.Model):
    role = models.ForeignKey("access.Role", on_delete=models.CASCADE)
    permission = models.ForeignKey("access.Permission", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("role", "permission")
        db_table = "iam_role_permission"
