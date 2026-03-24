
from .schema import Role

_ROLES = [
    Role(
        code="ghidora.viewer",
        name="Ghidora Viewer",
        policies=("ghidora.read_only",),
    ),
    Role(
        code="ghidora.admin",
        name="Ghidora Admin",
        policies=("ghidora.full",),
    ),
]

GHIDORA_ROLES = {r.code: r for r in _ROLES}