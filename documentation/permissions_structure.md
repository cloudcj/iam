project_root/
 ├── permissions/
 │    ├── schema.py        # Action, Resource, Service (dataclasses)
 │    ├── registry.py      # aggregated permission registry
 │    ├── policies.py      # policy bundles
 │    ├── validation.py    # startup validation
 │    ├── loaders.py       # (optional) seeding / sync helpers
 │    └── __init__.py
 ├── apps/
 │    ├── iam/
 │    │    └── permissions.py
 │    ├── inventory/
 │    │    └── permissions.py
 │    └── compute/
 └── manage.py



How policies work with many systems

Policies remain cross-system friendly.

Policy(
    name="infra.admin",
    permissions=(
        "inventory.*.*",
        "compute.*.*",
        "network.*.*",
    )
)


Or explicit:

permissions=(
    "inventory.az.read",
    "compute.vm.create",
)