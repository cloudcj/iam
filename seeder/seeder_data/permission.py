from ..constants import (
    InventoryPermissions,
    IAMPermissions,
    PLECOPermissions
)

# --------------------
# Permissions
# --------------------
PERMISSIONS = [
    # <permission_code>, <service>, <description>
    (IAMPermissions.USER_READ, "iam", "View users"),
    (IAMPermissions.USER_CREATE, "iam", "Create users"),
    (IAMPermissions.USER_UPDATE, "iam", "Modify users"),
    (IAMPermissions.USER_DELETE, "iam", "Delete user"),
    (IAMPermissions.USER_ASSIGN_ROLE, "iam", "Assign roles to users"),

    (InventoryPermissions.READ, "inventory", "Read inventory items"),
    (InventoryPermissions.UPDATE, "inventory", "Modify inventory items"),
    (InventoryPermissions.DELETE, "inventory", "Delete inventory items"),
 
    (PLECOPermissions.READ, "pleco", "View resources"),
    (PLECOPermissions.UPDATE, "pleco", "Modify resources"),
    (PLECOPermissions.DELETE, "pleco", "Delete reources")
]


