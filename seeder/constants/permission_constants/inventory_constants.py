class InventoryPermissions:
    """
    Inventory permission contracts.

    Naming:
      <system>.<resource>.<action>

    Rules:
    - *.access  → system entry
    - *.view    → pages + nav menu
    - *.create|update|delete → mutations
    """

    # --------------------
    # SYSTEM ACCESS
    # --------------------
    ACCESS = "inventory.access"

    # --------------------
    # VIEW (UI / NAV)
    # --------------------
    DASHBOARD_VIEW = "inventory.dashboard.view"
    REGIONS_VIEW = "inventory.regions.view"
    AZ_VIEW = "inventory.az.view"
    RACKS_VIEW = "inventory.racks.view"
    PODS_VIEW = "inventory.pods.view"
    SERVERS_VIEW = "inventory.servers.view"
    SWITCHES_VIEW = "inventory.switches.view"

    VIEW_ALL = [
        DASHBOARD_VIEW,
        REGIONS_VIEW,
        AZ_VIEW,
        RACKS_VIEW,
        PODS_VIEW,
        SERVERS_VIEW,
        SWITCHES_VIEW,
    ]

    # --------------------
    # ACTIONS
    # --------------------
    REGIONS_CREATE = "inventory.regions.create"
    REGIONS_UPDATE = "inventory.regions.update"
    REGIONS_DELETE = "inventory.regions.delete"

    RACKS_CREATE = "inventory.racks.create"
    RACKS_UPDATE = "inventory.racks.update"
    RACKS_DELETE = "inventory.racks.delete"

    SERVERS_CREATE = "inventory.servers.create"
    SERVERS_UPDATE = "inventory.servers.update"
    SERVERS_DELETE = "inventory.servers.delete"

    ACTION_ALL = [
        REGIONS_CREATE,
        REGIONS_UPDATE,
        REGIONS_DELETE,
        RACKS_CREATE,
        RACKS_UPDATE,
        RACKS_DELETE,
        SERVERS_CREATE,
        SERVERS_UPDATE,
        SERVERS_DELETE,
    ]

    # --------------------
    # ALL
    # --------------------
    ALL = [
        ACCESS,
        *VIEW_ALL,
        *ACTION_ALL,
    ]
