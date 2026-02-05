from django.contrib.auth import get_user_model

from ..seeder_data import SUPER_ADMIN
from apps.department.models import Department, UserDepartment
from apps.access.services.role_validation import validate_role_assignment
from apps.access.services.role_assignment import assign_role_to_user

User = get_user_model()


def seed_super_admin():
    data = SUPER_ADMIN

    user, created = User.objects.get_or_create(
        username=data["username"],
        defaults={
            "email": data["email"],
            "is_active": True,
        },
    )

    if created:
        user.set_password(data["password"])
        user.save()

    # 1️⃣ Assign department (structural invariant)
    department = Department.objects.get(code=data["department"])
    UserDepartment.objects.get_or_create(
        user=user,
        department=department,
    )

    # 2️⃣ Validate + assign role (NO BYPASS)
    role = validate_role_assignment(
        user=user,
        role_code=data["role"],  # SUPER_ADMIN
    )

    assign_role_to_user(
        user=user,
        role=role,
    )
