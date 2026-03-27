from .schema import Role

_ROLES = [
    Role(
        code="tropos.admin",
        name="Tropos Admin",
        policies=("tropos.full",),
    ),
    Role(
        code="tropos.operator", # no approval access
        name="Tropos Operator",
        policies=(
            "tropos.region.full",
            "tropos.az.full",
            "tropos.building.full",
            "tropos.device.full",
        ),
    ),
    Role(
        code="tropos.viewer",
        name="Tropos Viewer",
        policies=(
            "tropos.region.read_only",
            "tropos.az.read_only",
            "tropos.device.read_only",
            "tropos.building.read_only"
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
