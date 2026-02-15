from .schema import Policy
from ..services.helpers import all_permissions_for_service, read_permissions_for_service
from ..services.inventory import INVENTORY_SERVICE


INVENTORY_POLICIES = {
    "inventory.full_access": Policy(
        code="inventory.full_access",
        label="Inventory – Full Access",
        system="inventory",
        resource="*",
        permissions=all_permissions_for_service(INVENTORY_SERVICE),
        visible_in_ui=False,  # 🔥 hidden from checklist
    ),

    "inventory.read_all": Policy(
        code="inventory.read_all",
        label="Inventory – Read All",
        system="inventory",
        resource="*",
        permissions=read_permissions_for_service(INVENTORY_SERVICE),
        visible_in_ui=True,
    ),


    "inventory.az.read_only": Policy(
        code="inventory.az.read_only",
        label="AZ – Read only",
        system="inventory",
        resource="az",
        permissions=(
            "inventory.az.read",
        ),
        visible_in_ui=True
    ),

    "inventory.az.read_update": Policy(
        code="inventory.az.read_update",
        label="AZ – Read & Update",
        system="inventory",
        resource="az",
        permissions=(
            "inventory.az.read",
            "inventory.az.update",
        ),
        visible_in_ui=True
    ),

    "inventory.az.full": Policy(
        code="inventory.az.full",
        label="AZ – Full access",
        system="inventory",
        resource="az",
        permissions=(
            "inventory.az.read",
            "inventory.az.create",
            "inventory.az.update",
            "inventory.az.delete",
        ),
        visible_in_ui=True
    ),

    "inventory.device.read_only": Policy(
        code="inventory.device.read_only",
        label="Device – Read only",
        system="inventory",
        resource="az",
        permissions=(
            "inventory.device.read",
            "inventory.device.create",
            "inventory.device.update",
            "inventory.device.delete",
        ),
        visible_in_ui=True
    ),
}
