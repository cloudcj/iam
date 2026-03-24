from .schema import Policy
from ..helpers import all_permissions_for_service, read_permissions_for_service
from ..systems.tropos import TROPOS_SERVICE

_POLICIES = [
    # --------------------------------------------------
    # System-wide (used by platform roles)
    # --------------------------------------------------
    Policy(
        code="tropos.full",
        name="tropos – Full Access",
        system="tropos",
        resource="*",
        permissions=all_permissions_for_service(TROPOS_SERVICE),
        visible_in_ui=False,
    ),
    Policy(
        code="tropos.read_only",
        name="tropos – Read Only",
        system="tropos",
        resource="*",
        permissions=read_permissions_for_service(TROPOS_SERVICE),
        visible_in_ui=False,
    ),

    # --------------------------------------------------
    # AZ resource
    # --------------------------------------------------
    Policy(
        code="tropos.az.read_only",
        name="AZ – Read Only",
        system="tropos",
        resource="az",
        permissions=("tropos.az.read",),
    ),
    Policy(
        code="tropos.az.read_update",
        name="AZ – Read & Update",
        system="tropos",
        resource="az",
        permissions=(
            "tropos.az.read",
            "tropos.az.create",
            "tropos.az.update",
        ),
    ),
    Policy(
        code="tropos.az.full",
        name="AZ – Full Access",
        system="tropos",
        resource="az",
        permissions=(
            "tropos.az.read",
            "tropos.az.create",
            "tropos.az.update",
            "tropos.az.delete",
        ),
    ),

    # --------------------------------------------------
    # Device resource
    # --------------------------------------------------
    Policy(
        code="tropos.device.read_only",
        name="Device – Read Only",
        system="tropos",
        resource="device",
        permissions=("tropos.device.read",),
    ),
]

TROPOS_POLICIES = {p.code: p for p in _POLICIES}



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
