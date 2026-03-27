# from django.contrib.auth import get_user_model

# from apps.department.models import Department
# # from apps.access.services.role_validation import validate_role_assignment
# # from apps.access.services.role_assignment import assign_roles_to_user

# User = get_user_model()

# # seeder/seed_superadmin.py

# from django.contrib.auth import get_user_model
# from apps.department.models import Department

# User = get_user_model()


# def seed_superadmin():
#     """
#     Bootstrap the system superadmin.
#     - Department is REQUIRED
#     - No roles assigned
#     - Superadmin via is_superuser flag
#     """

#     department = Department.objects.get(code="GLOBAL")

#     user, created = User.objects.get_or_create(
#         username="SuperUser01",
#         defaults={
#             "first_name": "super",
#             "last_name": "user",
#             "email": "superuser01@test.com",
#             "is_active": True,
#             "is_staff": True,
#             "is_superuser": True,
#             "department": department,
#         },
#         username="SuperUser02",
#         defaults={
#             "first_name": "super",
#             "last_name": "user",
#             "email": "superuser01@test.com",
#             "is_active": True,
#             "is_staff": True,
#             "is_superuser": True,
#             "department": department,
#         },
#     )

#     if created:
#         user.set_password("Superuser@123")
#         user.save()



from django.contrib.auth import get_user_model
from apps.department.models import Department

User = get_user_model()


def seed_superadmin():
    """
    Bootstrap the system superadmins.
    - Department is REQUIRED
    - No roles assigned
    - Superadmin via is_superuser flag
    """

    department = Department.objects.get(code="GLOBAL")

    superusers = [
        ("SuperUser01", "superuser01@test.com"),
        ("SuperUser02", "superuser02@test.com"),
    ]

    for username, email in superusers:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "first_name": "Super",
                "last_name": "User",
                "email": email,
                "is_active": True,
                "is_staff": True,
                "is_superuser": True,
                "department": department,
            },
        )
        if created:
            user.set_password("Superuser@123")
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
