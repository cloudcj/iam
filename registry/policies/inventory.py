from .schema import Policy
from ..helpers import all_permissions_for_service, read_permissions_for_service
from ..systems.inventory import INVENTORY_SERVICE

_POLICIES = [
    # --------------------------------------------------
    # System-wide (used by platform roles)
    # --------------------------------------------------
    Policy(
        code="inventory.full",
        name="Inventory – Full Access",
        system="inventory",
        resource="*",
        permissions=all_permissions_for_service(INVENTORY_SERVICE),
        visible_in_ui=False,
    ),
    Policy(
        code="inventory.read_only",
        name="Inventory – Read Only",
        system="inventory",
        resource="*",
        permissions=read_permissions_for_service(INVENTORY_SERVICE),
        visible_in_ui=False,
    ),

    # --------------------------------------------------
    # AZ resource
    # --------------------------------------------------
    Policy(
        code="inventory.az.read_only",
        name="AZ – Read Only",
        system="inventory",
        resource="az",
        permissions=("inventory.az.read",),
    ),
    Policy(
        code="inventory.az.read_update",
        name="AZ – Read & Update",
        system="inventory",
        resource="az",
        permissions=(
            "inventory.az.read",
            "inventory.az.create",
            "inventory.az.update",
        ),
    ),
    Policy(
        code="inventory.az.full",
        name="AZ – Full Access",
        system="inventory",
        resource="az",
        permissions=(
            "inventory.az.read",
            "inventory.az.create",
            "inventory.az.update",
            "inventory.az.delete",
        ),
    ),

    # --------------------------------------------------
    # Device resource
    # --------------------------------------------------
    Policy(
        code="inventory.device.read_only",
        name="Device – Read Only",
        system="inventory",
        resource="device",
        permissions=("inventory.device.read",),
    ),
]

INVENTORY_POLICIES = {p.code: p for p in _POLICIES}



# INVENTORY_POLICIES = {
#     "inventory.full_access": Policy(
#         code="inventory.full_access",
#         name="Inventory – Full Access",
#         system="inventory",
#         resource="*",
#         permissions=all_permissions_for_service(INVENTORY_SERVICE),
#         visible_in_ui=False,  # 🔥 hidden from checklist
#     ),

#     "inventory.read_all": Policy(
#         code="inventory.read_all",
#         name="Inventory – Read All",
#         system="inventory",
#         resource="*",
#         permissions=read_permissions_for_service(INVENTORY_SERVICE),
#         visible_in_ui=True,
#     ),


#     "inventory.az.read_only": Policy(
#         code="inventory.az.read_only",
#         name="AZ – Read only",
#         system="inventory",
#         resource="az",
#         permissions=(
#             "inventory.az.read",
#         ),
#         visible_in_ui=True
#     ),

#     "inventory.az.read_update": Policy(
#         code="inventory.az.read_update",
#         name="AZ – Read & Update",
#         system="inventory",
#         resource="az",
#         permissions=(
#             "inventory.az.read",
#             "inventory.az.update",
#         ),
#         visible_in_ui=True
#     ),

#     "inventory.az.full": Policy(
#         code="inventory.az.full",
#         name="AZ – Full access",
#         system="inventory",
#         resource="az",
#         permissions=(
#             "inventory.az.read",
#             "inventory.az.create",
#             "inventory.az.update",
#             "inventory.az.delete",
#         ),
#         visible_in_ui=True
#     ),

#     "inventory.device.read_only": Policy(
#         code="inventory.device.read_only",
#         name="Device – Read only",
#         system="inventory",
#         resource="device",
#         permissions=(
#             "inventory.device.read",
#             "inventory.device.create",
#             "inventory.device.update",
#             "inventory.device.delete",
#         ),
#         visible_in_ui=True
#     ),
# }
