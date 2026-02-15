🌍 Gaia Platform – IAM-Centric Authorization Architecture

# 🔐 Core Philosophy

We use centralized IAM authorization with identity-only JWTs.

- JWT = identity only (user_id, username, iss, aud)
- Permissions are NOT trusted from JWT
- IAM DB is the single source of truth
- All services call IAM to authorize
- Frontend visibility is permission-driven
- Roles are presets → policies
- Policies expand → permissions

Design principle:

    JWT authenticates
    IAM authorizes
    Services enforce
    Frontend reflects


# 🧱 Data Model (IAM)

Department

- Has allowed_roles (via DepartmentAllowedRole)

Role

- Has RolePolicy
- Roles are presets (UI checklist)
- Not stored on user permanently (we expand them)

Policy

- Bundle of permissions

Example:

    inventory.az.read_update

PolicyPermission

- Expands policy → concrete permissions

Permission

- Canonical string:

    inventory.az.read

User

- Has department
- Has UserPolicy (authoritative access)
- No user-role relationship stored
- Roles expand → policies at assignment time

# 🧠 Permission Resolution

Effective permissions are resolved through:

    UserPolicy
        ↓
    PolicyPermission
        ↓
    Permission

Core check:

    user.has_permission(permission_code)

Used by:

    IAM /authorize
    IAM /authorize/batch
    System permission classes

# Login Flow

Endpoint (IAM)

    POST /api/login/

Flow:

    1.) authenticate()
    2.) resolve_user_effective_permissions()
    3.) issue_user_tokens()
    4.) JWT stored in HTTP-only cookie

JWT contains:

    {
    "sub": "user-id",
    "username": "alice",
    "iss": "gaia-iam",
    "aud": "gaia-api"
    }

Permissions in JWT are ignored.

# 🏢 System Visibility (Layer 1)
Endpoint (IAM)

    GET /api/me/systems/

Logic:

- Get effective permissions
- Extract system prefix (inventory, monitoring)
- Return unique systems

Example response:

    {
        "systems": [
            { "code": "inventory", "label": "Inventory" }
        ]
    }

Controls navbar visibility.

# 📂 Navigation Visibility (Layer 2)
Endpoint (Per system)

    GET /inventory/api/navigation/

Each system has a NAVIGATION registry:

    NAVIGATION = [
        {
            "path": "/inventory/devices",
            "label": "Devices",
            "permission": "inventory.device.read",
        }
    ]

Flow:

    1.) Collect all route permissions
    2.) Call IAM /authorize/batch
    3.) Filter routes based on allowed permissions
    4.) Return allowed routes only

Frontend renders sidebar.

# 🛡 API Enforcement (Layer 3)

Each ViewSet:

    permission_classes = [IsAuthenticated, IAMPermission]
    required_permission = "inventory.device.read"

IAMPermission:

- Calls IAM /authorize
- IAM calls user.has_permission()
- Returns True/False
- 403 if denied

Even if frontend is bypassed, backend is secure.

# 🔄 Cross-Service Communication

Inventory → IAM:

    POST /api/iam/authorize/
    POST /api/iam/authorize/batch/

Cookies forwarded.

IAM validates:

- RS256 signature
- Issuer
- Audience

Services never access IAM DB directly.

# 🎯 Current Working State

✅ Identity-only JWT (RS256)
✅ IAM centralized authorization
✅ Department → Role → Policy governance
✅ UserPolicy authoritative storage
✅ /authorize working
✅ /authorize/batch working
✅ /navigation working
✅ /me/systems designed
✅ Microservice separation clean

# 🏗 Final Architecture

    Login → IAM
        ↓
    /me/systems → IAM (navbar visibility)
        ↓
    /navigation → Inventory (route visibility)
        ↓
    API call → Inventory
        ↓
    IAMPermission → IAM authorize
        ↓
    Allowed / 403

# 🧠 Key Design Decisions

- No permissions stored in JWT
- No user-role relationship stored
- Roles are presets only
- Policies are bundles
- Permissions are atomic
- IAM is single source of truth
- Systems remain independent