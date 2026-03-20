from apps.access.models import Policy
from registry.policies import POLICIES_REGISTRY
from .seed_policy_permissions import seed_policy_permissions

def seed_policies():
    for policy in POLICIES_REGISTRY.values():
        policy_obj, _ = Policy.objects.update_or_create(
            code=policy.code,
            defaults={
                "name": policy.name,
                "system": policy.system,
                "resource": policy.resource,
                "description": (
                    f"Grants {policy.name} access "
                    # f"to {policy.system.upper()} "
                    # f"{policy.resource.upper()}"
                ),
            },
        )

        seed_policy_permissions(policy_obj, policy)


# policy description format

# Grants <Label> access to <System> <Resource>
