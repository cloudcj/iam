# STEP 0 — Freeze (Do NOT Touch These Yet)

Before we start, do NOT change:

- RS256
- cookie-based JWT
- auth middleware
- existing role assignments
- existing API permission checks
  Your system works. We’re layering, not breaking.

# 🟢 STEP 1 — Define Permission Constants (START HERE)

This is the foundation. Everything else depends on this.

Create one file per system.

inventory/permissions.py

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

✅ This step alone does nothing functional yet.
✅ That’s intentional.

# 🟢 STEP 2 — Seed Permissions into DB (No Behavior Change)

Because you store permissions in DB, sync them once.

Management command / migration

    from inventory.permissions import InventoryPermissions
    from iam.models import Permission

    def seed_inventory_permissions():
        for code in InventoryPermissions.ALL:
            Permission.objects.get_or_create(
                code=code,
                defaults={
                    "system": "inventory",
                    "description": code,
                }
            )

🚫 Do NOT delete old permissions yet
🚫 Do NOT change role mappings yet

# 🟢 STEP 3 — Attach VIEW Permissions to Existing Roles

Now you make roles menu-aware.

Inventory Viewer

    inventory.access
    inventory.dashboard.view
    inventory.regions.view
    inventory.az.view
    inventory.racks.view
    inventory.servers.view

Inventory Admin

    inventory.access
    ALL inventory.*.view
    ALL inventory.*.create/update/delete

👉 Admin and Viewer see same menus, different power.

# 🟢 STEP 4 — Create Menu Registry (Backend Only)
Create a menu table (or constants).

    | key       | label     | path                 | permission               |
    | --------- | --------- | -------------------- | ------------------------ |
    | dashboard | Dashboard | /inventory/dashboard | inventory.dashboard.view |
    | regions   | Regions   | /inventory/regions   | inventory.regions.view   |
    | az        | AZ        | /inventory/az        | inventory.az.view        |
    | racks     | Racks     | /inventory/racks     | inventory.racks.view     |
    | servers   | Servers   | /inventory/servers   | inventory.servers.view   |

Menus never reference roles.

# 🟢 STEP 5 — Implement /me/inventory
Backend logic:

    permissions = resolve_permissions(user)

    menu = Menu.objects.filter(
        permission__in=permissions,
        system="inventory"
    )

    return {
        "permissions": permissions,
        "menu": menu
    }

Test with Postman.
No frontend yet.

# 🟢 STEP 6 — Frontend: Sidebar Only
Only now touch React.

- Call /me
- Call /me/inventory
- Render menu from response

Do NOT touch API calls yet.

# 🟢 STEP 7 — Button Visibility
Add checks like:

    hasPermission("inventory.regions.delete")

# 🟡 STEP 8 — (Optional, Later) Retire inventory.read

Only after everything works:

- replace inventory.read with specific .view
migrate slowly
keep compatibility during transition

🧠 THE MOST IMPORTANT RULE (Read Twice)

- At no point should you redesign auth while doing UI permissions.

You are adding clarity, not changing security.

## 🧠 Final Checklist (If You Feel Lost)

If you’re unsure what to do next, ask yourself:

✔ Did I define permission constants?
✔ Did I seed them?
✔ Did I assign .view to roles?
✔ Did I create menu → permission mapping?
✔ Did /me/{system} work?

If yes → move forward.
If not → stop and fix only that step.