# 🌍 Gaia Runtime Flow (After Login)

We’ll start from the moment the user submits credentials.

# 1️⃣ Login (IAM)

Endpoint (IAM)

    POST /api/login/

Backend Flow

Inside IAM:

    login()
        → authenticate()
        → resolve_user_effective_permissions()
        → issue_user_tokens()

What Happens

    1.) Validate username/password
    2.)  Check user is active
    3.)  Resolve policies → permissions (for audit / optional embedding)
    4.) Issue JWT (RS256 signed)
    5.)  Set JWT in HTTP-only cookie

JWT Contains:

    {
    "sub": "user-id",
    "username": "alice",
    "iss": "gaia-iam",
    "aud": "gaia-api"
    }

🚨 JWT permissions are not trusted by services.

# 2️⃣ Get Visible Systems (Navbar Level)

Frontend calls (IAM)

    GET /api/me/systems/

Backend Flow (IAM)

    MeSystemsView.get()
        → get_visible_systems_for_user(user)


Inside service:

    Permission.objects
        .filter(permission_policies__policy__policy_users__user=user)

Extract prefix:

    inventory.device.read → inventory


Return unique systems.

Response

    {
        "systems": [
            { "code": "inventory", "label": "Inventory" }
        ]
    }


Frontend renders navbar with only allowed systems.

# 3️⃣ User Clicks Inventory

Frontend loads Inventory module.

Calls:

    GET /inventory/api/navigation/

# 4️⃣ Inventory Navigation Flow

Inventory View

    NavigationView.get()

## Step 1 — Collect Required Permissions

    permission_codes = [
        route["permission"] for route in NAVIGATION
    ]

Example:

    [
        "inventory.device.read",
        "inventory.az.read",
        "inventory.region.read"
    ]

## Step 2 — Batch Check With IAM

    batch_check_permissions(request, permission_codes)

Makes HTTP call:

    POST /api/iam/authorize/batch/

Body:

    {
    "permissions": [...]
    }

Cookies forwarded.

# 5️⃣ IAM Batch Authorize

Endpoint

    POST /api/iam/authorize/batch/

View
BatchAuthorizeView.post()


Logic:

allowed = [
    perm for perm in permissions
    if user.has_permission(perm)
]

# 6️⃣ Permission Resolution

Inside IAM:

    user.has_permission(permission_code)

Delegates to:

    AuthorizationService.has_permission()

Checks:

    UserPolicy
        ↓
    PolicyPermission
        ↓
    Permission

Returns True / False.

No JWT logic involved.

# 7️⃣ IAM Returns Allowed Permissions

Example:

    {
        "allowed": ["inventory.az.read"]
    }

# 8️⃣ Inventory Filters Routes

    allowed_routes = [
        route for route in NAVIGATION
        if route["permission"] in allowed_permissions
    ]

Response:

    {
    "system": "inventory",
    "label": "Inventory",
    "routes": [
        {
        "path": "/inventory/az",
        "label": "Availability Zones"
        }
    ]
}


Frontend renders sidebar.

# 9️⃣ User Clicks a Page (Devices)

Frontend loads:

    /inventory/devices

Component calls:

    GET /api/devices/

# 10️⃣ DeviceViewSet Authorization

class DeviceViewSet:
    permission_classes = [IsAuthenticated, IAMPermission]
    required_permission = "inventory.device.read"

# 11️⃣ IAMPermission Executes

Inside Inventory:

    allowed = check_permission(request, required_permission)

Calls IAM:

    POST /api/iam/authorize/

IAM:

user.has_permission("inventory.device.read")

Returns:

- 200 if allowed
- 403 if denied

# Full Runtime Flow (Condensed Diagram)

    Login → IAM
        ↓
    /me/systems → IAM (system visibility)
        ↓
    Click Inventory
        ↓
    /inventory/navigation → Inventory
        ↓
    Inventory → IAM /authorize/batch
        ↓
    IAM → user.has_permission()
        ↓
    Allowed routes returned
        ↓
    Click Devices
        ↓
    GET /api/devices/
        ↓
    Inventory → IAM /authorize
        ↓
    IAM → user.has_permission()
        ↓
    Allowed or 403

# Layered Authorization Model

    Layer	|    Endpoint	 |   Responsibility
    ---------------------------------------------
    Layer 1	 |   /me/systems |	System visibility
    Layer 2	 |  /navigation	 |  Route visibility
    Layer 3	 |  /authorize	 |  API enforcement

Each layer protects a different boundary.

🔒 Security Properties

✅ JWT is identity-only
✅ Permissions always checked against IAM DB
✅ Immediate revocation works
✅ Systems never store permission logic
✅ Navigation is dynamic
✅ API is always protected

Even if frontend is manipulated:

Backend enforcement blocks access.

# Architectural Separation

## IAM Owns

- Identity
- Roles
- Policies
- Permissions
- Authorization decisions
- System visibility

## Systems Own

- Business logic
- Navigation registry
- API endpoints
- Enforcement via IAMPermission

🎯 Where You Are Now

You have fully working:

- Centralized IAM
- Distributed microservices
- Cookie-based RS256 JWT
- Dynamic system visibility
- Dynamic navigation
- Centralized authorization enforcement

This is enterprise-grade RBAC.

# Next Enhancements

- Add caching layer to reduce IAM calls
- Add service-to-service trust hardening
- Add audit logging for authorization decisions
- Add performance tuning
-efine governance rules (department → role → policy)