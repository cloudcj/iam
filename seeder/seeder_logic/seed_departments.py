from apps.department.models import Department
from registry.departments import DEPARTMENT_REGISTRY


def seed_departments():
    for dept in DEPARTMENT_REGISTRY.values():
        Department.objects.get_or_create(
            code=dept.code,
            defaults={
                "name": dept.name,
            },
        )
