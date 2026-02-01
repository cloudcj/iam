# apps/department/services/department_service.py

from django.db import transaction
from django.core.exceptions import ValidationError

from apps.department.models import Department, UserDepartment


@transaction.atomic
def create_department(*, actor, name, parent=None):
    if not actor.is_superuser:
        raise ValidationError("Not allowed")

    return Department.objects.create(
        name=name,
        parent=parent,
    )


@transaction.atomic
def assign_user_to_department(*, actor, user, department):
    if not actor.is_superuser:
        raise ValidationError("Not allowed")

    UserDepartment.objects.update_or_create(
        user=user,
        defaults={"department": department},
    )


# what should be in department service:

# create_department
# update_department
# archive_department
# restore_department

# assign_user_to_department
# remove_user_from_department
# transfer_user_department
# get_user_department

# update_department_metadata
# set_department_manager
