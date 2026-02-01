# identity/models/role.py
import uuid
from django.db import models


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    code = models.CharField( max_length=64,unique=True,db_index=True,help_text="Stable system identifier (DO NOT CHANGE)")
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    permissions = models.ManyToManyField(
        "access.Permission",
        through="RolePermission",
        related_name="roles",
    )

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'iam_role'
