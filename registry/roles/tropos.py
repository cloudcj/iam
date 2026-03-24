from .schema import Role

_ROLES = [
    Role(
        code="tropos.viewer",
        name="Tropos Viewer",
        policies=(
            "tropos.az.read_only",
            "tropos.device.read_only",
        ),
    ),
    Role(
        code="tropos.admin",
        name="Tropos Admin",
        policies=(
            # "tropos.az.full",
            # "tropos.device.read_only",
            "tropos.full",
        ),
    ),
]

TROPOS_ROLES = {r.code: r for r in _ROLES}

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
