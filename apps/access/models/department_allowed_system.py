from django.db import models


class DepartmentAllowedSystem(models.Model):
    department = models.ForeignKey(
        "department.Department",
        on_delete=models.CASCADE,
        related_name="allowed_system_entries",
    )
    system = models.CharField(max_length=50)

    class Meta:
        unique_together = ("department", "system")
        db_table = "iam_department_allowed_system"
