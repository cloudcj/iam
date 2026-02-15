from apps.department.models import Department
from apps.access.models import Role
from access_control.departments import DEPARTMENT_REGISTRY


def seed_department_allowed_roles():
    for dept in DEPARTMENT_REGISTRY.values():

        db_department = Department.objects.get(code=dept.name)

        roles = Role.objects.filter(code__in=dept.allowed_roles)

        if roles.count() != len(dept.allowed_roles):
            existing = set(roles.values_list("code", flat=True))
            missing = set(dept.allowed_roles) - existing
            raise RuntimeError(
                f"Department {dept.name} references missing roles: {missing}"
            )

        # ✅ Correct field name
        db_department.allowed_roles.set(roles)
