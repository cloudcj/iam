from apps.department.models import Department
from apps.access.models import Role, DepartmentAllowedRole

from ..seeder_data import DEPARTMENT_ALLOWED_ROLES


# --------------------
# Department → Allowed Roles
# --------------------
def seed_department_allowed_roles():
    for dept_code, role_names in DEPARTMENT_ALLOWED_ROLES.items():
        department = Department.objects.get(code=dept_code)

        for role_name in role_names:
            role = Role.objects.get(code=role_name)
            DepartmentAllowedRole.objects.get_or_create(
                department=department,
                role=role,
            )
