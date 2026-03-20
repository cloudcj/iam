# permissions/policies/global.py
from .schema import Role

# _ROLES = [
#     Role(
#         code="global.readonly",
#         name="Global Viewer",
#         policies=("global.viewer",),
#     ),
# ]

# GLOBAL_ROLES = {r.code: r for r in _ROLES}

# GLOBAL_ROLES = {
#     "global.readonly": Role(
#         code="global.readonly",
#         name="Global Viewer",
#         policies=("global.viewer",),
#     )
# }


_ROLES = [
    Role(
        code="platform.admin",
        name="Platform Admin",
        policies=(
            "inventory.full",
            "iam.full",
            # add each system's full policy as you add systems
        ),
    ),
    Role(
        code="platform.viewer",
        name="Platform Viewer",
        policies=(
            "inventory.read_only",
            "iam.read_only",
            # add each system's read_only policy as you add systems
        ),
    ),
]

GLOBAL_ROLES = {r.code: r for r in _ROLES}
