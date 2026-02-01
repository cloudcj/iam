from seeder.constants import RoleCodes,IAMPermissions,InventoryPermissions,PLECOPermissions

# --------------------
# Roles
# --------------------
ROLES = [
    # <role_name>, <description>
    # IAM
    (RoleCodes.PLATFORM_ADMIN, "Platform Admin", "Full platform access"),
    # INVENTORY
    (RoleCodes.INVENTORY_VIEWER, "Inventory Viewer", "Read-only inventory access"),
    (RoleCodes.INVENTORY_ADMIN, "Inventory Admin","Full inventory access"),
    # PLECO
    (RoleCodes.PLECO_ADMIN, "Pleco Admin","Read-only pleco access"),
    (RoleCodes.PLECO_VIEWER, "Pleco Viewer","Full access pleco access"),
]


# --------------------
# Role → Permission mapping
# --------------------
ROLE_PERMISSIONS = {
    # <role_name>: [<permission_code>, ...]
    # IAM
    RoleCodes.PLATFORM_ADMIN: [
        IAMPermissions.USER_READ,
        IAMPermissions.USER_CREATE,
        IAMPermissions.USER_UPDATE,
        IAMPermissions.USER_ASSIGN_ROLE,

        InventoryPermissions.ALL,
        PLECOPermissions.ALL,

    ],
    # INVENTORY
    RoleCodes.INVENTORY_VIEWER: [
        InventoryPermissions.READ,
    ],
    RoleCodes.INVENTORY_ADMIN: [
        InventoryPermissions.ALL
    ],
    # PLECO
    RoleCodes.PLECO_VIEWER: [
        PLECOPermissions.READ,
    ],
    RoleCodes.PLECO_ADMIN: [
        PLECOPermissions.ALL
    ],
}