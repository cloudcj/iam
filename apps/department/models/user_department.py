# iam/models/user_department.py
from django.db import models


class UserDepartment(models.Model):
    user = models.ForeignKey("identity.User", on_delete=models.CASCADE, related_name="user_department")
    department = models.ForeignKey("department.Department", on_delete=models.CASCADE)

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "department")
        db_table = "iam_user_department"
