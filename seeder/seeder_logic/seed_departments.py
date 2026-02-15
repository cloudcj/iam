from apps.department.models import Department
from access_control.departments import DEPARTMENT_REGISTRY


def seed_departments():
    for dept in DEPARTMENT_REGISTRY.values():
        Department.objects.update_or_create(
            code=dept.name,
            defaults={
                "name": dept.label,
            },
        )
