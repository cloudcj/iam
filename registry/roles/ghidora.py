
from .schema import Role

_ROLES = [
    Role(
        code="ghidora.admin",
        name="Ghidora Admin",
        policies=("ghidora.full",),
    ),
    Role(
        code="ghidora.operator", # no approval access
        name="Ghidora Operator",
        policies=("ghidora.dashboard.full",),
    ),
    Role(
        code="ghidora.viewer",
        name="Ghidora Viewer",
        policies=("ghidora.read_only",),
    ),
    
]

GHIDORA_ROLES = {r.code: r for r in _ROLES}