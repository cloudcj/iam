from django.db import models


class DepartmentAllowedRole(models.Model):
    department = models.ForeignKey(
        "department.Department",
        on_delete=models.CASCADE,
        related_name="allowed_roles",
    )
    role = models.ForeignKey(
        "access.Role",
        on_delete=models.CASCADE,
        related_name="allowed_departments",
    )

    class Meta:
        db_table = "iam_department_allowed_role"
        unique_together = ("department", "role")
