# from django.db import models


# class DepartmentAllowedRole(models.Model):
#     department = models.ForeignKey(
#         "department.Department",
#         on_delete=models.CASCADE,
#         related_name="allowed_roles",
#     )
#     role = models.ForeignKey(
#         "access.Role",
#         on_delete=models.CASCADE,
#         related_name="allowed_departments",
#     )

#     class Meta:
#         db_table = "iam_department_allowed_role"
#         unique_together = ("department", "role")

# identity/models/department_allowed_role.py
from django.db import models


class DepartmentAllowedRole(models.Model):
    department = models.ForeignKey(
        "department.Department",
        on_delete=models.CASCADE,
    )
    role = models.ForeignKey(
        "access.Role",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("department", "role")
        indexes = [
            models.Index(fields=["department"]),
            models.Index(fields=["role"]),
        ]
        db_table = "iam_department_allowed_role"
