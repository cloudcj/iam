# from authz.models import Role, Permission
# from ..seeder_data import rbac_data

# def seed_rbac():
#     """
#     Create roles and permissions and link them.
#     Safe to run multiple times.
#     """
#     for role_name, perm_codes in rbac_data.items():
#         role, _ = Role.objects.get_or_create(name=role_name)

#         for code in perm_codes:
#             perm, _ = Permission.objects.get_or_create(code=code)
#             role.permissions.add(perm)

#     print("✅ RBAC seeded successfully")
