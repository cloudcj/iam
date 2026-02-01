# # iam/bootstrap/seed.py

# from django.contrib.auth import get_user_model

# from iam.models import (
#     Department,
#     Permission,
#     Role,
#     RolePermission,
#     DepartmentAllowedRole,
#     UserDepartment,
#     UserRole,
# )

# from iam.bootstrap.data import (
#     DEPARTMENTS,
#     PERMISSIONS,
#     ROLES,
#     ROLE_PERMISSIONS,
#     DEPARTMENT_ALLOWED_ROLES,
#     SUPER_ADMIN,
# )

# User = get_user_model()


# # --------------------
# # Departments
# # --------------------
# def seed_departments():
#     for code, name in DEPARTMENTS:
#         Department.objects.get_or_create(
#             code=code,
#             defaults={"name": name},
#         )


# # --------------------
# # Permissions
# # --------------------
# def seed_permissions():
#     for code, service, description in PERMISSIONS:
#         Permission.objects.get_or_create(
#             code=code,
#             defaults={
#                 "service": service,
#                 "description": description,
#             },
#         )


# # --------------------
# # Roles
# # --------------------
# def seed_roles():
#     for name, description in ROLES:
#         Role.objects.get_or_create(
#             name=name,
#             defaults={"description": description},
#         )


# # --------------------
# # Role → Permission mapping
# # --------------------
# def seed_role_permissions():
#     for role_name, perm_codes in ROLE_PERMISSIONS.items():
#         role = Role.objects.get(name=role_name)

#         for perm_code in perm_codes:
#             permission = Permission.objects.get(code=perm_code)
#             RolePermission.objects.get_or_create(
#                 role=role,
#                 permission=permission,
#             )


# # --------------------
# # Department → Allowed Roles
# # --------------------
# def seed_department_allowed_roles():
#     for dept_code, role_names in DEPARTMENT_ALLOWED_ROLES.items():
#         department = Department.objects.get(code=dept_code)

#         for role_name in role_names:
#             role = Role.objects.get(name=role_name)
#             DepartmentAllowedRole.objects.get_or_create(
#                 department=department,
#                 role=role,
#             )


# # --------------------
# # Super Admin
# # --------------------
# def seed_super_admin():
#     user, created = User.objects.get_or_create(
#         username=SUPER_ADMIN["username"],
#         defaults={
#             "email": SUPER_ADMIN["email"],
#             "is_staff": True,
#             "is_superuser": True,
#         },
#     )

#     if created:
#         user.set_password(SUPER_ADMIN["password"])
#         user.save()

#     department = Department.objects.get(code=SUPER_ADMIN["department"])
#     role = Role.objects.get(name=SUPER_ADMIN["role"])

#     UserDepartment.objects.get_or_create(
#         user=user,
#         department=department,
#     )

#     UserRole.objects.get_or_create(
#         user=user,
#         role=role,
#     )


# # --------------------
# # MASTER ENTRYPOINT
# # --------------------
# def run_iam_bootstrap():
#     seed_departments()
#     seed_permissions()
#     seed_roles()
#     seed_role_permissions()
#     seed_department_allowed_roles()
#     seed_super_admin()
