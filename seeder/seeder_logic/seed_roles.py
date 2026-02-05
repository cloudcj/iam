from apps.access.models import Role, Permission, RolePermission
from ..seeder_data import ROLES, ROLE_PERMISSIONS


def seed_roles():
    for code, name, description in ROLES:
        Role.objects.get_or_create(
            code=code,
            defaults={
                "name": name,
                "description": description,
            },
        )




# --------------------
# Roles
# --------------------
# def seed_roles():
#     for name, description in ROLES:
#         Role.objects.get_or_create(
#             name=name,
#             defaults={"description": description},
#         )

# --------------------
# Role → Permission mapping
# --------------------
# def seed_role_permissions():
#     for role_code, perm_codes in ROLE_PERMISSIONS.items():
#         role = Role.objects.get(code=role_code)

#         for perm_code in perm_codes:
#             permission = Permission.objects.get(code=perm_code)
#             RolePermission.objects.get_or_create(
#                 role=role,
#                 permission=permission,
#             )



def seed_role_permissions():
    for role_code, perm_entries in ROLE_PERMISSIONS.items():
        role = Role.objects.get(code=role_code)

        for entry in perm_entries:

            # Normalize to a SET (handles .ALL and single permissions)
            if isinstance(entry, (list, tuple, set)):
                perm_codes = set(entry)
            else:
                perm_codes = {entry}

            for perm_code in perm_codes:
                permission = Permission.objects.get(code=perm_code)

                RolePermission.objects.get_or_create(
                    role=role,
                    permission=permission,
                )



# def seed_role_permissions():
#     for role_code, perm_entries in ROLE_PERMISSIONS.items():
#         role = Role.objects.get(code=role_code)

#         for entry in perm_entries:

#             # CASE 1: ALL permissions (list)
#             if isinstance(entry, (list, tuple, set)):
#                 perm_codes = entry
#             else:
#                 perm_codes = [entry]

#             for perm_code in perm_codes:
#                 permission = Permission.objects.get(code=perm_code)

#                 RolePermission.objects.get_or_create(
#                     role=role,
#                     permission=permission,
#                 )


