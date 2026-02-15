from django.contrib.auth import get_user_model

from apps.department.models import Department, UserDepartment
# from apps.access.services.role_validation import validate_role_assignment
# from apps.access.services.role_assignment import assign_roles_to_user

User = get_user_model()

# seeder/seed_superadmin.py

from django.contrib.auth import get_user_model
from apps.department.models import Department

User = get_user_model()


def seed_superadmin():
    """
    Bootstrap the system superadmin.
    - Department is REQUIRED
    - No roles assigned
    - Superadmin via is_superuser flag
    """

    department = Department.objects.get(code="CLOUD_PLATFORM")

    user, created = User.objects.get_or_create(
        username="SuperAdmin",
        defaults={
            "email": "admin@gaia.test",
            "is_active": True,
            "is_staff": True,
            "is_superuser": True,
            "department": department,
        },
    )

    if created:
        user.set_password("Superadmin123!")
        user.save()



# def seed_superadmin():
#     department = Department.objects.get(code="CLOUD_PLATFORM")

#     user, created = User.objects.get_or_create(
#         username="superadmin",
#         defaults={
#             "email": "admin@gaia.test",
#             "is_active": True,
#             "is_staff": True,
#             "is_superuser": True,
#             "department": department,
#         },
#     )

#     if created:
#         import os
#         password = os.getenv("SUPERADMIN_PASSWORD")
#         if not password:
#             raise RuntimeError("SUPERADMIN_PASSWORD not set")

#         user.set_password(password)
#         user.save()
