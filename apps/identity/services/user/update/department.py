
# from django.db import transaction
# from django.core.exceptions import ValidationError

# from apps.identity.models import User
# from apps.department.models import Department


# @transaction.atomic
# def update_user_department(*, user_id, department_code):
#     try:
#         user = User.objects.select_for_update().get(id=user_id)
#     except User.DoesNotExist:
#         raise ValidationError("User not found")

#     try:
#         department = Department.objects.get(code=department_code)
#     except Department.DoesNotExist:
#         raise ValidationError("Invalid department")

#     user.department = department
#     user.save(update_fields=["department"])
#     return user
# # @transaction.atomic
# # def update_user_department(*, user, department_code):
# #     try:
# #         department = Department.objects.get(code=department_code)
# #     except Department.DoesNotExist:
# #         raise ValidationError("Invalid department")

# #     UserDepartment.objects.update_or_create(
# #         user=user,
# #         defaults={"department": department},
# #     )

from django.db import transaction
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.department.models import Department


@transaction.atomic
def update_user_department(
    *,
    actor: AbstractBaseUser,
    target: AbstractBaseUser,
    department_code: str,
):
    # ❌ no self-update
    if actor.id == target.id:
        raise PermissionDenied("You cannot update your own department")

    # 🔐 superuser only
    if not actor.is_superuser:
        raise PermissionDenied("Only superusers can change department")

    # 🔎 resolve department
    try:
        department = Department.objects.get(code=department_code)
    except Department.DoesNotExist:
        raise ValidationError("Invalid department")

    # 🔁 update department FK directly
    target.department = department
    target.save(update_fields=["department"])

    return True