from .schema import Role

_ROLES = [
    Role(
        code="inventory.viewer",
        name="Inventory – Viewer",
        policies=(
            "inventory.az.read_only",
            "inventory.device.read_only",
        ),
    ),
    Role(
        code="inventory.admin",
        name="Inventory – Admin",
        policies=(
            "inventory.az.full",
            "inventory.device.read_only",
        ),
    ),
]

INVENTORY_ROLES = {r.code: r for r in _ROLES}

# INVENTORY_ROLES = {
#     "inventory.viewer": Role(
#         code="inventory.viewer",
#         name="Inventory – Viewer",
#         policies=(
#             "inventory.az.read_only",
#             "inventory.device.read_only"

#         ),
#     ),

#     "inventory.admin": Role(
#         code="inventory.admin",
#         name="Inventory – Admin",
#         policies=(
#             "inventory.az.full",
#             "inventory.device.read_only"
#         ),
#     ),
# }
