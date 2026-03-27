from .schema import make_system

GHIDORA_SERVICE = make_system(
    name="ghidora",
    label="Ghidora",
    resources={
        "dashboard": ("Dashboard", ["read", "create", "update", "delete"]),
        "approval":  ("Approval",   ["read","update"]),
    },
)