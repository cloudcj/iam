from .schema import Role


INVENTORY_ROLES = {
    "inventory.viewer": Role(
        code="inventory.viewer",
        label="Inventory – Viewer",
        policies=(
            "inventory.az.read_only",
            "inventory.device.read_only"

        ),
    ),

    "inventory.admin": Role(
        code="inventory.admin",
        label="Inventory – Admin",
        policies=(
            "inventory.az.full",
            "inventory.device.read_only"
        ),
    ),
}
