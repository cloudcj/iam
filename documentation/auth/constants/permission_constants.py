class InventoryPermissions:
    READ = "inventory.read"
    UPDATE = "inventory.update"
    DELETE = "inventory.delete"

    # ALL = {READ,UPDATE,DELETE}

    ALL = [
        READ,
        UPDATE,
        DELETE,
    ]

class IAMPermissions:
    USER_READ = "iam.user.read"
    USER_CREATE = "iam.user.create"
    USER_UPDATE = "iam.user.update"
    USER_ASSIGN_ROLE = "iam.user.assign_role"

class PLECOPermissions:
    READ = "pleco.read"
    UPDATE = "pleco.update"
    DELETE = "pleco.delete"

    # ALL = {READ,UPDATE,DELETE}

    ALL = [
        READ,
        UPDATE,
        DELETE,
    ]