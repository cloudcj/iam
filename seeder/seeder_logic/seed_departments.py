from apps.department.models import Department
from ..seeder_data import DEPARTMENTS

# --------------------
# Departments
# --------------------
def seed_departments():
    for code, name in DEPARTMENTS:
        Department.objects.get_or_create(
            code=code,
            defaults={"name": name},
        )

