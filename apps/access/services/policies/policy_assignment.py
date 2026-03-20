from django.db import transaction

from apps.access.models import (
    Policy,
    UserPolicy,
)

@transaction.atomic
def assign_policies_to_user(user, policy_codes: list[str]):

    policies = Policy.objects.filter(code__in=policy_codes)

    if policies.count() != len(policy_codes):
        existing = set(policies.values_list("code", flat=True))
        missing = set(policy_codes) - existing
        raise RuntimeError(f"Invalid policies: {missing}")

    # 1️⃣ Get allowed roles for department
    allowed_roles = user.department.roles.all()

    # 2️⃣ Get allowed policies via those roles
    allowed_policies = Policy.objects.filter(
        policy_roles__role__in=allowed_roles
    ).distinct()

    allowed_policy_codes = set(
        allowed_policies.values_list("code", flat=True)
    )

    if not set(policy_codes).issubset(allowed_policy_codes):
        raise RuntimeError(
            "One or more policies are not allowed for this department"
        )

    # 3️⃣ Replace state
    UserPolicy.objects.filter(user=user).delete()

    UserPolicy.objects.bulk_create(
        [
            UserPolicy(user=user, policy=policy)
            for policy in policies
        ]
    )
