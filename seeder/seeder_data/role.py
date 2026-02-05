from seeder.constants import RoleCodes,IAMPermissions,InventoryPermissions,PLECOPermissions

# --------------------
# Roles
# --------------------
ROLES = [
    # <role_name>, <description>
    # IAM
    (RoleCodes.IAM_ADMIN, "Platform Admin", "Full platform access"),
    # INVENTORY
    (RoleCodes.INVENTORY_VIEWER, "Inventory Viewer", "Read-only inventory access"),
    (RoleCodes.INVENTORY_ADMIN, "Inventory Admin","Full inventory access"),
    # PLECO
    (RoleCodes.PLECO_ADMIN, "Pleco Admin","Read-only pleco access"),
    (RoleCodes.PLECO_VIEWER, "Pleco Viewer","Full access pleco access"),
    # GLOBAL
    (RoleCodes.SUPER_ADMIN, "Super Admin","Global system administrator with unrestricted access"),
    # SUPER ADMIN
    (RoleCodes.GLOBAL_VIEWER, "Global viewer","Global viewer with unrestricted access"),
]

# # Roles that bypass department scoping
# GLOBAL_ROLES = {
#     RoleCodes.SUPER_ADMIN,
#     RoleCodes.GLOBAL_VIEWER
# }


# --------------------
# Role → Permission mapping
# --------------------
ROLE_PERMISSIONS = {
    # <role_name>: [<permission_code>, ...]

    # SUPER ADMIN
    RoleCodes.SUPER_ADMIN: [
        IAMPermissions.USER_READ,
        IAMPermissions.USER_CREATE,
        IAMPermissions.USER_UPDATE,
        IAMPermissions.USER_DELETE,
        IAMPermissions.USER_ASSIGN_ROLE,

        InventoryPermissions.ALL,
        PLECOPermissions.ALL,

    ],

    # GLOBAL VIEWER
    RoleCodes.GLOBAL_VIEWER: [
        InventoryPermissions.READ,
        PLECOPermissions.READ,

    ],

    # IAM ADMIN
    RoleCodes.IAM_ADMIN: [
        IAMPermissions.USER_READ,
        IAMPermissions.USER_CREATE,
        IAMPermissions.USER_UPDATE,
        IAMPermissions.USER_DELETE,
        IAMPermissions.USER_ASSIGN_ROLE,

    ],
    # INVENTORY
    RoleCodes.INVENTORY_VIEWER: [
        IAMPermissions.USER_READ,
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