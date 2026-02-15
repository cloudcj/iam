from apps.access.models import Role,RolePermission, PolicyPermission
from access_control.roles.registry import ROLES_REGISTRY
from .seed_role_policies import seed_role_policies

def seed_roles():
    for role_def in ROLES_REGISTRY.values():
        role_obj, _ = Role.objects.update_or_create(
            code=role_def.code,
            defaults={
                "name": role_def.label,
                "description": (
                    f"Role providing {role_def.label} access"
                ),
            },
        )

        seed_role_policies(role_obj, role_def)


def seed_role_permissions():
    """
    Expand Role → Policy → Permission into RolePermission
    (derived runtime authorization table)
    """

    # Derived data → safe to regenerate
    RolePermission.objects.all().delete()

    # Policy → Permission
    for pp in PolicyPermission.objects.select_related("policy", "permission"):
        # Policy → Role
        for rp in pp.policy.policy_roles.select_related("role"):
            RolePermission.objects.get_or_create(
                role=rp.role,
                permission=pp.permission,
            )




# def seed_role_permissions():
#     for role in ROLES.values():
#         db_role = Role.objects.get(name=role.name)

#         permission_codes = set()

#         for policy_name in role.policies:
#             policy = POLICIES[policy_name]
#             permission_codes.update(policy.permissions)

#         permissions = Permission.objects.filter(
#             code__in=permission_codes
#         )

#         db_role.permissions.set(permissions)


# def seed_role_permissions():
#     for role in ROLES.values():
#         db_role = Role.objects.get(code=role.code)  # ✅ FIX

#         permission_codes = set()
#         for policy_code in role.policies:
#             policy = POLICIES[policy_code]
#             permission_codes.update(policy.permissions)

#         permissions = Permission.objects.filter(code__in=permission_codes)
#         db_role.permissions.set(permissions)




# def seed_role_permissions():
#     """
#     Expand Role → Policy → Permission into RolePermission.
#     Derived data only — safe to regenerate.
#     """

#     # Clear existing derived permissions
#     RolePermission.objects.all().delete()

#     # Policy → Permission
#     for pp in PolicyPermission.objects.select_related("policy", "permission"):
#         # Role → Policy
#         for rp in pp.policy.role_policies.select_related("role"):
#             RolePermission.objects.get_or_create(
#                 role=rp.role,
#                 permission=pp.permission,
#             )
