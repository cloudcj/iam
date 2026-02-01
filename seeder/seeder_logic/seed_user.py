from apps.access.models import Role,UserRole
from apps.identity.models import User
from apps.department.models import Department,UserDepartment

from ..seeder_data import SUPER_ADMIN

# --------------------
# Super Admin
# --------------------
def seed_super_admin():
    user, created = User.objects.get_or_create(
        username=SUPER_ADMIN["username"],
        defaults={
            "email": SUPER_ADMIN["email"],
            "is_staff": True,
            "is_superuser": True,
        },
    )

    if created:
        user.set_password(SUPER_ADMIN["password"])
        user.save()

    department = Department.objects.get(code=SUPER_ADMIN["department"])
    role = Role.objects.get(code=SUPER_ADMIN["role"])

    UserDepartment.objects.get_or_create(
        user=user,
        department=department,
    )

    UserRole.objects.get_or_create(
        user=user,
        role=role,
    )
