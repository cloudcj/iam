# Edit User — Form Logic & API Reference

## Overview

The Edit User modal (`EditUserModal.tsx`) allows platform admins and superusers to update a user's basic info, roles, and direct permissions. The permission checkboxes reflect the selected roles in real time — no extra API calls needed when switching roles.

---

## APIs Used

### On Modal Open (fetched in parallel)

| Hook | Endpoint | Purpose |
|---|---|---|
| `useGetMeQuery()` | `GET /api/v1/me/` | Determine actor role (superuser / platform admin / dept admin) |
| `useGetDepartmentsQuery()` | `GET /api/v1/department/` | Populate department dropdown |
| `useGetPermissionsQuery()` | `GET /api/v1/access/permissions/` | Full permission list — used to build the checkbox grid |
| `useGetUserQuery(user.id)` | `GET /api/v1/identity/users/:id/` | Fetch `permission_ids`, `role_permission_ids`, `direct_permission_ids` for the target user |

### When Department is Selected

| Hook | Endpoint | Purpose |
|---|---|---|
| `useGetRoleFormOptionsQuery(departmentId)` | `GET /api/v1/access/roles/form-options/?department=:id` | Returns available management roles + system roles scoped to that department, including their policies and `grants_systems` |

### On Save

| Hook | Endpoint | Payload |
|---|---|---|
| `useUpdateUserMutation()` | `PATCH /api/v1/identity/users/:id/update/` | `{ first_name, last_name, email, department, roles: [...roleIds], permission_ids: [...directPermIds] }` |

---

## State

```typescript
const [managementRole, setManagementRole] = useState<string | null>(null)
const [systemRoles, setSystemRoles] = useState<Record<string, string>>({})
const [directPermIds, setDirectPermIds] = useState<string[]>([])
```

| State | Type | Description |
|---|---|---|
| `managementRole` | `string \| null` | Selected management role **code** (e.g. `"platform.admin"`) |
| `systemRoles` | `Record<string, string>` | Map of `{ system: roleId }` (e.g. `{ iam: "uuid-123" }`) |
| `directPermIds` | `string[]` | Only manually assigned extra permissions — role-derived perms are never stored here |

---

## On Modal Open — Initialization

```typescript
// superuser — controls all permissions directly
if (isSuperuser)     setDirectPermIds(userDetail.permission_ids)

// platform admin — only loads their manually-added extras
if (isPlatformAdmin) setDirectPermIds(userDetail.direct_permission_ids)
```

- `userDetail` comes from `useGetUserQuery`
- `permission_ids` — all permissions (role + direct)
- `direct_permission_ids` — only SOURCE_DIRECT permissions

---

## `rolePermIds` — Derived, Never Stored

```typescript
const rolePermIds = useMemo(() =>
  new Set(computePermissionsFromRoles(managementRole, systemRoles))
, [managementRole, systemRoles])
```

`computePermissionsFromRoles()` walks `managementRole + systemRoles → policies → permission_codes → permission IDs` using data already in `formOptions` (from `useGetRoleFormOptionsQuery`). Recomputes automatically on every role change — **no extra API call**.

---

## When Management Role Changes

```typescript
// Role with grants (e.g. platform.admin grants iam, tropos systems)
→ auto-selects matching system roles (admin/viewer suffix)
→ isSuperuser:     setDirectPermIds(computePermissionsFromRoles(newRole, autoSysRoles))
→ isPlatformAdmin: setDirectPermIds([])   // direct perms cleared — must re-add manually

// Role cleared (set to None)
→ systemRoles cleared
→ directPermIds cleared
```

**Design decision:** When a platform admin changes the management role, direct permissions are intentionally cleared. Role-derived permissions automatically reflect via `rolePermIds`. This prevents stale direct assignments from carrying over to an unrelated role.

---

## What the Permission Checkbox Sees

```typescript
checked  = rolePermIds.has(p.id) || directPermIds.includes(p.id)
disabled = rolePermIds.has(p.id)   // role perms: auto-checked, cannot be toggled
```

- **Role permissions** → greyed out, auto-checked, reflect current role selection
- **Direct permissions** → editable checkboxes, stored in `directPermIds`
- The two never mix in state — only combined visually for display

---

## On Save

```typescript
permission_ids: directPermIds   // only direct perms sent
roles: [...roleIds]             // backend re-derives SOURCE_ROLE perms from this
```

- No filtering needed — `directPermIds` only contains direct perms by design
- Backend (`update_user` service) deletes all existing permissions and re-inserts:
  - `SOURCE_ROLE` — derived from the submitted `roles` array
  - `SOURCE_DIRECT` — from the submitted `permission_ids`

---

## Full Flow

```
useGetMeQuery()
    → actor is platform.admin
    → canAssignDirect = true  (permission section shown)

useGetUserQuery(id)
    → userDetail.direct_permission_ids
    → setDirectPermIds(direct_permission_ids)      ← initial state

useGetPermissionsQuery()
    → allPermissions (full list)
    → used to render checkboxes + compute role→permission mapping

useGetRoleFormOptionsQuery(deptId)
    → formOptions.management_roles[].policies[].permission_codes
    → used by computePermissionsFromRoles()
    → rolePermIds = derived from this + current role selections

Role changed by user:
    → computePermissionsFromRoles() re-runs (no API call, uses formOptions cache)
    → rolePermIds recomputes → greyed checkboxes update instantly
    → isPlatformAdmin: directPermIds = []

On save:
    → PATCH sends roles[] + directPermIds[]
    → backend re-derives SOURCE_ROLE perms from roles[]
    → backend stores SOURCE_DIRECT perms from directPermIds[]
```

---

## Actor Permission Matrix

| Actor | Can edit roles | Can edit direct perms | On role change |
|---|---|---|---|
| Superuser | Yes (all roles) | Yes (full control) | Presets checkboxes from new role |
| Platform Admin | Yes (excl. platform.admin) | Yes (extras only) | Clears direct perms |
| Dept Admin | Yes (dept-scoped) | No | N/A |
