# import uuid
# from django.db import models


# class Permission(models.Model):
#     """
#     Atomic permission.
#     Example: inventory.read, ticket.create
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

#     code = models.CharField(
#         max_length=100,
#         unique=True,
#         db_index=True
#     )
#     description = models.TextField(blank=True)

#     def __str__(self):
#         return self.code

# identity/models/permission.py
import uuid
from django.db import models


class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    code = models.CharField(max_length=150, unique=True)  
    # example: inventory.read

    system = models.CharField(max_length=50)
    resource = models.CharField(max_length=50)
    action = models.CharField(max_length=50)


    description = models.TextField(blank=True)

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'iam_permission'
