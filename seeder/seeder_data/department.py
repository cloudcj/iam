# iam/bootstrap/data.py
from ..constants import RoleCodes,IAMPermissions,InventoryPermissions,DepartmentCodes

# --------------------
# Departments
# ------------------
DEPARTMENTS = [
    # <department_code>, <department_name>
    (DepartmentCodes.CLOUD_PLATFORM, "Cloud Platform"),
    (DepartmentCodes.CLOUD_SOLUTIONS, "Cloud Solutions"),
    (DepartmentCodes.CLOUD_MONITORING, "Cloud Monitoring"),
]

# --------------------
# Department → Allowed Roles
# --------------------
DEPARTMENT_ALLOWED_ROLES = {
    # <department_code>: [<role_name>, ...]
    DepartmentCodes.CLOUD_PLATFORM: [
        RoleCodes.IAM_ADMIN,
        RoleCodes.INVENTORY_ADMIN,
        RoleCodes.PLECO_ADMIN
    ],
    DepartmentCodes.CLOUD_SOLUTIONS : [
        RoleCodes.INVENTORY_VIEWER,
        RoleCodes.PLECO_VIEWER
    ],
    DepartmentCodes.CLOUD_MONITORING: [
        RoleCodes.PLECO_ADMIN
    ],
}



# def seed_departments():
#     for code, name in DEPARTMENTS:
#         obj, created = Department.objects.get_or_create(
#             code=code,
#             defaults={"name": name},
#         )

#         if created:
#             print(f"[IAM] Created department: {code}")

# # iam/bootstrap/seed.py

# from iam.models import Department
# from iam.bootstrap.data import DEPARTMENTS


# def seed_departments():
#     for code, name in DEPARTMENTS:
#         Department.objects.get_or_create(
#             code=code,
#             defaults={"name": name},
#         )
