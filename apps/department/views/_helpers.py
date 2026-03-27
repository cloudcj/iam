from apps.department.models import Department
from apps.access.models import DepartmentAllowedSystem


def dept_data(department):
    return {
        "id": str(department.id),
        "code": department.code,
        "name": department.name,
        "allowed_systems": department.allowed_systems,
    }


def set_allowed_systems(department, systems):
    DepartmentAllowedSystem.objects.filter(department=department).delete()
    DepartmentAllowedSystem.objects.bulk_create(
        [DepartmentAllowedSystem(department=department, system=s) for s in systems],
        ignore_conflicts=True,
    )
