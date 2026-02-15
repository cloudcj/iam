# permissions/seeder/seed_policy_permissions.py
from apps.access.models import Policy, Permission, PolicyPermission
from access_control.policies import POLICIES_REGISTRY


def seed_policy_permissions(policy_obj, policy_def):

    # 🔐 Collect validated permission objects
    permission_objs = []
    for perm_code in policy_def.permissions:
        try:
            permission = Permission.objects.get(code=perm_code)
        except Permission.DoesNotExist:
            raise RuntimeError(
                f"Missing permission '{perm_code}' "
                f"referenced by policy '{policy_def.code}'"
            )
        permission_objs.append(permission)

    # 🧹 Remove stale mappings
    PolicyPermission.objects.filter(policy=policy_obj).delete()

    # 🔁 Recreate mappings exactly
    for permission in permission_objs:
        PolicyPermission.objects.create(
            policy=policy_obj,
            permission=permission,
        )


# def seed_policy_permissions():
#     for policy_def in POLICIES.values():
#         policy = Policy.objects.get(code=policy_def.code)

#         for perm_code in policy_def.permissions:
#             try:
#                 permission = Permission.objects.get(code=perm_code)
#             except Permission.DoesNotExist:
#                 raise RuntimeError(
#                     f"Missing permission '{perm_code}' "
#                     f"referenced by policy '{policy_def.code}'"
#                 )

#             PolicyPermission.objects.get_or_create(
#                 policy=policy,
#                 permission=permission,
#             )

# def seed_policy_permissions():
#     for policy_def in POLICIES.values():
#         policy = Policy.objects.get(code=policy_def.code)

#         # 🔐 Collect validated permission objects
#         permission_objs = []
#         for perm_code in policy_def.permissions:
#             try:
#                 permission = Permission.objects.get(code=perm_code)
#             except Permission.DoesNotExist:
#                 raise RuntimeError(
#                     f"Missing permission '{perm_code}' "
#                     f"referenced by policy '{policy_def.code}'"
#                 )
#             permission_objs.append(permission)

#         # 🧹 Remove stale mappings
#         PolicyPermission.objects.filter(policy=policy).delete()

#         # 🔁 Recreate mappings exactly
#         for permission in permission_objs:
#             PolicyPermission.objects.create(
#                 policy=policy,
#                 permission=permission,
#             )
