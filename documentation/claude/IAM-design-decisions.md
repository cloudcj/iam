# IAM System Design Decisions

This document captures all finalized design decisions from the design sessions.
This supersedes and extends the older IAM-roles.md and IAM-user_creation.md where there are conflicts.

---

## 1. Access Control Model — Permission-Based (with Role/Policy UI presets)

This system uses **Permission-Based Access Control** at runtime.
Roles and policies are **UI convenience presets only** — they are never checked at authorization time.

```
Assignment time:  Role → Policy → Permission → UserPermission (saved)
Runtime:          UserPermission → JWT permissions[]
```

| Concept | Purpose |
|---|---|
| Role | UI preset — selects a bundle of policies for convenience |
| Policy | UI preset — selects a bundle of permissions for convenience |
| UserRole | Stored for UI display and reporting only — never checked at auth time |
| UserPermission | **Source of truth** — individual permissions saved per user, what goes into JWT |
| Permission | Individual action code (e.g. `inventory.az.read`) |

### Key rules
- Roles and policies are **never** checked at authorization time
- Only `UserPermission` rows determine what a user can do
- A role could be deleted and the user would still have their permissions via `UserPermission`
- `source` field on `UserPermission` tracks origin: `"role"` (from role preset) or `"direct"` (manually added at update time)

### Why permissions as source of truth (not policies)
- **1-hop resolution** at login: `UserPermission → JWT` (vs 4-hop chain with policies)
- **Native fine-grained control**: removing one permission = deleting one row
- **Future flexibility**: JWT payload can switch from permissions to policy codes by changing one query in the token service — `UserPermission` stays untouched
- **Simpler update logic**: no need for override models, just add/remove rows

---

## 2. Role Hierarchy

```
Tier 0 — Superuser           Django is_superuser=True, bypasses all checks
Tier 1 — platform.admin      All systems, all departments, goes through checks
Tier 1 — platform.viewer     Read-only, all systems, all departments
Tier 2 — dept.admin          IAM user management, own department only
Tier 2 — dept.viewer         Read-only IAM, own department only
Tier 3 — {system}.admin      Full access, specific system
Tier 3 — {system}.viewer     Read-only, specific system
```

### Hidden roles — cannot be seen or assigned by dept.admin

```python
HIDDEN_FROM_IAM_ADMIN = {
    "platform.admin",
    "platform.viewer",
    "dept.admin",
    "dept.viewer",
}
```

---

## 3. IAM Permissions

```
iam.user.read
iam.user.create          — initial creation including role and dept assignment
iam.user.update          — basic info (name, email, password, status)
iam.user.delete
iam.user.update_role     — change an existing user's roles (post-creation)
iam.user.update_policy   — change an existing user's permissions (post-creation)
iam.user.update_dept     — move an existing user to a different department
iam.user.assign_policy   — add permissions to a user (post-creation)
iam.user.remove_policy   — remove permissions from a user (post-creation)

iam.department.read
iam.department.update_systems   — manage which systems a department can access
```

### Clarification — create vs update_*

`iam.user.create` covers the initial role assignment and department at creation time.
`update_role`, `update_policy`, `update_dept`, `assign_policy`, `remove_policy` are strictly
post-creation update operations.

---

## 4. Policy Naming Convention

Format: `{system}.{resource}.{level}` for resource-specific
Format: `{system}.{level}` for system-wide

Access levels:
- `read_only` — read only
- `manage` — full CRUD without department transfer
- `full` — all operations including department transfer

### IAM Policies

| Code | Permissions | Used by |
|---|---|---|
| `iam.read_only` | all iam.*.read (system-wide) | platform.viewer |
| `iam.full` | all iam.* permissions (system-wide) | platform.admin |
| `iam.user.read_only` | iam.user.read | dept.viewer |
| `iam.user.manage` | read, create, update, delete, update_role, update_policy, assign_policy, remove_policy | dept.admin |

Note: `iam.user.manage` does NOT include `update_dept` — dept.admin cannot move users between departments.

### Inventory Policies

| Code | Permissions | Used by |
|---|---|---|
| `inventory.read_only` | all inventory.*.read (system-wide) | platform.viewer |
| `inventory.full` | all inventory.* permissions (system-wide) | platform.admin |
| `inventory.az.read_only` | inventory.az.read | inventory.viewer |
| `inventory.az.full` | all az permissions | inventory.admin |
| `inventory.device.read_only` | inventory.device.read | inventory.viewer |

---

## 5. Roles → Policies Mapping

```
platform.admin   →  iam.full + inventory.full + {system}.full per system
platform.viewer  →  iam.read_only + inventory.read_only + {system}.read_only per system

dept.admin       →  iam.user.manage
dept.viewer      →  iam.user.read_only

inventory.admin  →  inventory.az.full + inventory.device.read_only
inventory.viewer →  inventory.az.read_only + inventory.device.read_only
```

At runtime, these all expand to individual `UserPermission` rows.

---

## 6. User Creation Rules

### Superuser
- Created via seeder/code only — never through the API
- `User.objects.create_user()` never sets `is_superuser=True` — impossible via API by design
- Can create any user in any department
- Can assign any role including platform.admin
- Department is required (use GLOBAL for platform-level users)
- No role scope restrictions

### Platform Admin
- Can create any user in any department
- Can assign any role EXCEPT `platform.admin`
- Roles must be within the department's `allowed_systems`
- Department is required
- Cannot create another platform.admin — superuser only

### Department Admin
- Department is auto-set to actor's own department — input ignored
- Can only assign non-hidden roles within dept's allowed systems
- Role validation: `role.code.split(".")[0]` must be in `department.allowed_systems`
- Hidden role validation: `role.code` must NOT be in `HIDDEN_FROM_IAM_ADMIN`
- Cannot add extra permissions at creation — locked to role's permissions only
- Cannot move users between departments

### Role assignment authority summary

| Role to assign | Superuser | Platform Admin | Dept Admin |
|---|---|---|---|
| platform.admin | ✅ | ❌ | ❌ |
| platform.viewer | ✅ | ❌ | ❌ |
| dept.admin | ✅ | ✅ | ❌ |
| dept.viewer | ✅ | ✅ | ❌ |
| {system}.admin/viewer | ✅ | ✅ (dept scoped) | ✅ (dept scoped) |

---

## 7. Permission Assignment at Creation vs Update

### Creation time
```
Role selected → auto-expands: Role → Policy → Permission → UserPermission (source="role")
No manual permission selection at creation — roles only
Dept admin: locked to role permissions only
```

### Update time (post-creation)
```
Superuser:       can add/remove any permission (including role-based), no scope limit
Platform Admin:  can add/remove any permission within department scope (including role-based)
Dept Admin:      role change only — no direct permission control
```

### Why permissions cannot be unchecked at creation
Creation is always predictable — you get exactly what the role gives.
Fine-grained control belongs at update time, not creation time.

### UI behavior at update time
Policies still appear in the UI as **presets for bulk-adding permissions**.
Selecting a policy preset bulk-checks its permissions — but the API receives only permission UUIDs.
The policy itself is never saved to DB.

---

## 8. Department System Access

### DepartmentAllowedSystem
Controls which operational systems a department can access.
Used for:
1. Dept admin and platform admin role scope validation at creation time
2. Auto-checking systems in UI when department is selected
3. Filtering which system roles are visible in UI

### Important — IAM is NOT in DepartmentAllowedSystem
IAM access is role-driven, not department-driven.
```
dept.admin in CLOUD_SOLUTIONS → gets IAM access via their role
NOT because CLOUD_SOLUTIONS has "iam" in allowed_systems
```

### DepartmentAllowedSystem only tracks operational systems
```python
Department(code="GLOBAL",           allowed_systems=("inventory",))
Department(code="CLOUD_PLATFORM",   allowed_systems=("inventory",))
Department(code="CLOUD_SOLUTIONS",  allowed_systems=("inventory",))
Department(code="CLOUD_MONITORING", allowed_systems=("inventory",))
```

### Registry vs DB
Registry defines default/initial state only.
Seeder uses `get_or_create` — never deletes existing entries.
UI (platform admin) can add systems to departments after initial seed.
DB is the source of truth at runtime.

---

## 9. UI Design — User Creation Form

### Management Role section (superuser and platform admin only)
Separate from system roles. Covers platform-level and dept-level management roles.

```
Management Role: [None ▼]
                  None
                  ─────────────────
                  Department Viewer
                  Department Admin
                  ─────────────────   ← superuser only
                  Platform Viewer
                  Platform Admin
```

Visibility rules:
- Superuser → sees all four options
- Platform Admin → sees dept.viewer and dept.admin only
- Dept Admin → section hidden entirely

### System Roles section
One role per system. Systems shown are based on department's allowed_systems.

```
inventory → [Inventory Admin  ▼]
ticketing → [Ticketing Viewer ▼]
```

One role per system is enforced — having inventory.admin AND inventory.viewer
simultaneously makes no sense as admin already includes viewer access.

### Permissions section (display only at creation)
Auto-selected from chosen roles. Grouped by system > resource > permission.
- All actors: permissions are display only at creation, cannot be customized
- Fine-grained permission control happens at update time only

### Allowed systems display (superuser and platform admin only)
When a department is selected, its allowed systems are shown as informational display.
Not a selectable input — purely descriptive.
Dept admin does not see this section.

### At least one role required
```
if management_role is None and no system roles selected:
    → error: "User must have at least one role"
```

---

## 10. IAM as a Backend Concept Only

IAM is not a selectable system in the UI system roles section.
The user management page itself IS the IAM system from the user's perspective.

| Context | IAM role |
|---|---|
| DepartmentAllowedSystem | Not included |
| System roles UI section | Not shown |
| Management role section | Lives here (dept.admin etc.) |
| Registry (backend) | Still exists — generates permissions and policies |
| JWT permissions | Embedded (iam.user.read etc.) |

---

## 11. Permission Constants

```python
class IAMPermissions:
    USER_READ          = "iam.user.read"
    USER_CREATE        = "iam.user.create"
    USER_UPDATE        = "iam.user.update"
    USER_DELETE        = "iam.user.delete"
    USER_UPDATE_ROLE   = "iam.user.update_role"
    USER_UPDATE_POLICY = "iam.user.update_policy"
    USER_UPDATE_DEPT   = "iam.user.update_dept"
    USER_ASSIGN_POLICY = "iam.user.assign_policy"
    USER_REMOVE_POLICY = "iam.user.remove_policy"
```

---

## 12. User Visibility Rules

| Actor | Can see |
|---|---|
| Superuser | All users across all departments |
| Platform Admin | All users across all departments |
| Platform Viewer | All users across all departments |
| Dept Admin | Only users in their department, excluding hidden role users |
| Dept Viewer | Only users in their department, excluding hidden role users |

### Dept Admin visibility exclusion
Dept admin cannot see users with hidden roles in their department:
```python
qs.filter(department=actor.department)
  .exclude(user_roles__role__code__in=HIDDEN_FROM_IAM_ADMIN)
```

### Always excluded from listing
Superusers (`is_superuser=True`) are always excluded from listing regardless of actor.
