from apps.access.models import Role as RoleModel, Policy, RolePolicy
from registry.roles import ROLES_REGISTRY  # aggregated IAM + inventory + etc


def seed_role_policies(role_obj, role_def):

    # 🔐 Validate policies exist
    policy_objs = []
    for policy_code in role_def.policies:
        try:
            policy = Policy.objects.get(code=policy_code)
        except Policy.DoesNotExist:
            raise RuntimeError(
                f"Missing policy '{policy_code}' "
                f"referenced by role '{role_def.code}'"
            )
        policy_objs.append(policy)

    # 🧹 Remove stale mappings
    RolePolicy.objects.filter(role=role_obj).delete()

    # 🔁 Recreate mappings
    RolePolicy.objects.bulk_create(
        [
            RolePolicy(role=role_obj, policy=p)
            for p in policy_objs
        ]
    )



# def seed_role_policies():
#     for role_def in ROLES.values():
#         role = RoleModel.objects.get(code=role_def.code)

#         # 🔐 Validate policies exist
#         policy_objs = []
#         for policy_code in role_def.policies:
#             try:
#                 policy = Policy.objects.get(code=policy_code)
#             except Policy.DoesNotExist:
#                 raise RuntimeError(
#                     f"Missing policy '{policy_code}' "
#                     f"referenced by role '{role_def.code}'"
#                 )
#             policy_objs.append(policy)

#         # 🧹 Remove stale mappings
#         RolePolicy.objects.filter(role=role).delete()

#         # 🔁 Recreate exact mappings
#         for policy in policy_objs:
#             RolePolicy.objects.create(
#                 role=role,
#                 policy=policy,
#             )
