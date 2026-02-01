

# rbac_data = {
#     # 🔐 IAM OWNER — FULL CONTROL
#     "SuperAdmin": [
#         # IAM / Identity
#         "iam.user.read",
#         "iam.user.write",
#         "iam.user.create",
#         "iam.user.delete",

#         # RBAC
#         "iam.role.read",
#         "iam.role.write",
#         "iam.role.assign",

#         # Tokens / Security
#         "iam.token.issue",
#         "iam.token.revoke",
#     ],

#     # 🛠 APPLICATION ADMIN — NO IAM CONTROL
#     "Admin": [
#         "inventory.read",
#         "inventory.write",
#         "report.view",
#     ],

#     # 👤 REGULAR USER
#     "Member": [
#         "inventory.read",
#         "report.view",
#     ],

#     # 👀 READ-ONLY USER
#     "Viewer": [
#         "report.view",
#     ],
# }


# # def seed_rbac():
# #     """
# #     Create roles and permissions and link them.
# #     Safe to run multiple times.
# #     """
# #     for role_name, perm_codes in RBAC_DEFINITION.items():
# #         role, _ = Role.objects.get_or_create(name=role_name)

# #         for code in perm_codes:
# #             perm, _ = Permission.objects.get_or_create(code=code)
# #             role.permissions.add(perm)

# #     print("✅ RBAC seeded successfully")
