# Edit User

## Overview

Updates an existing user's basic info, roles, and direct permissions. Permission checkboxes reflect the selected roles in real time — no extra API calls needed when switching roles.

**Frontend:** `EditUserModal.tsx`  
**Permission required:** `iam.user.update` or superuser

---

## API Reference

### Update User

```
PATCH /api/v1/identity/users/:id/update/
```

**Auth:** JWT cookie or `Authorization: Bearer <token>`  
**Permission:** `iam.user.update` or superuser

#### Request Body

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "jdoe@example.com",
  "is_active": true,
  "department": "uuid",
  "roles": ["uuid", "uuid"],
  "permission_ids": ["uuid", "uuid"],
  "username": "jdoe"
}
```

#### Request Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `first_name` | string | Yes | |
| `last_name` | string | Yes | |
| `email` | string | Yes | Must be unique |
| `is_active` | boolean | No | Default `true` |
| `department` | UUID | Yes | |
| `roles` | UUID[] | Yes | Backend re-derives `SOURCE_ROLE` permissions from this |
| `permission_ids` | UUID[] | No | Direct permissions only (`SOURCE_DIRECT`) — superuser / platform admin only |
| `username` | string | No | Superuser only |

#### Response `200 OK`

```json
{
  "id": "uuid",
  "username": "jdoe",
  "first_name": "John",
  "last_name": "Doe",
  "email": "jdoe@example.com",
  "is_active": true
}
```

#### Error Responses

| Status | Reason |
|---|---|
| `400` | Validation error (duplicate email, invalid role) |
| `403` | Actor lacks `iam.user.update` permission |
| `404` | User not found |

---

### Supporting Endpoints (used by the form)

#### Get User Detail
```
GET /api/v1/identity/users/:id/
```
Returns the target user's current permissions, split by source:

```json
{
  "id": "uuid",
  "username": "jdoe",
  "permission_ids": ["uuid", ...],
  "role_permission_ids": ["uuid", ...],
  "direct_permission_ids": ["uuid", ...]
}
```

| Field | Description |
|---|---|
| `permission_ids` | All permissions (role + direct) |
| `role_permission_ids` | Only `SOURCE_ROLE` permissions |
| `direct_permission_ids` | Only `SOURCE_DIRECT` permissions |

#### Get All Permissions
```
GET /api/v1/access/permissions/
```
Full permission list — used to render the checkbox grid.

#### Get Role Form Options
```
GET /api/v1/access/roles/form-options/?department=<uuid>
```
Returns management roles and system roles scoped to the department, including their policies and `grants_systems`. Used to compute `rolePermIds` when roles change.

---

## Actor Restrictions

| Actor | Can edit username | Can edit roles | Can edit direct perms | On role change |
|---|---|---|---|---|
| Superuser | Yes | Yes (all roles) | Yes (full control) | Presets checkboxes from new role |
| Platform Admin | No | Yes (excl. `platform.admin`) | Yes (extras only) | Clears direct perms |
| Dept Admin | No | Yes (dept-scoped) | No | N/A |

---

## Backend Reference

### Service (`apps/identity/services/user/update/full.py`)

`update_user()` performs:
1. Updates basic user fields (`first_name`, `last_name`, `email`, `is_active`, `department`)
2. Optionally updates `username` (superuser only)
3. Deletes all existing `UserPermission` records for the user
4. Bulk-creates `UserPermission` with `source=SOURCE_ROLE` — derived from submitted `roles`
5. Bulk-creates `UserPermission` with `source=SOURCE_DIRECT` — from submitted `permission_ids`
6. Deletes and recreates `UserRole` records from submitted `roles`

### Serializer (`apps/identity/serializers/user/update.py`)

```python
first_name     = CharField()
last_name      = CharField()
email          = EmailField()
is_active      = BooleanField(required=False)
department     = UUIDField()
roles          = ListField(child=UUIDField())
permission_ids = ListField(child=UUIDField(), required=False)
username       = CharField(required=False)   # superuser only
```

### Audit Log

On success, logs `user.update` with `detail: { "username": "<username>" }`.

---

## Frontend Reference

### RTK Query Hooks

| Hook | Endpoint | When |
|---|---|---|
| `useGetMeQuery()` | `GET /api/v1/me/` | On mount — determines actor role |
| `useGetUserQuery(id)` | `GET /api/v1/identity/users/:id/` | On modal open — loads current perms |
| `useGetDepartmentsQuery()` | `GET /api/v1/department/` | On mount — populates department dropdown |
| `useGetPermissionsQuery()` | `GET /api/v1/access/permissions/` | On mount — builds checkbox grid |
| `useGetRoleFormOptionsQuery(deptId)` | `GET /api/v1/access/roles/form-options/?department=:id` | When department is selected |
| `useUpdateUserMutation()` | `PATCH /api/v1/identity/users/:id/update/` | On save |

### State

```typescript
const [managementRole, setManagementRole] = useState<string | null>(null)
const [systemRoles, setSystemRoles] = useState<Record<string, string>>({})
const [directPermIds, setDirectPermIds] = useState<string[]>([])
```

| State | Type | Description |
|---|---|---|
| `managementRole` | `string \| null` | Selected management role code |
| `systemRoles` | `Record<string, string>` | `{ system: roleId }` — one role per system |
| `directPermIds` | `string[]` | Manually assigned direct permissions only — role-derived perms are never stored here |

### Initialization (on modal open)

```typescript
// superuser — controls all permissions directly
if (isSuperuser)     setDirectPermIds(userDetail.permission_ids)

// platform admin — loads only manually-added extras
if (isPlatformAdmin) setDirectPermIds(userDetail.direct_permission_ids)
```

### `rolePermIds` — Derived, Never Stored

```typescript
const rolePermIds = useMemo(() =>
  new Set(computePermissionsFromRoles(managementRole, systemRoles))
, [managementRole, systemRoles])
```

Walks `managementRole + systemRoles → policies → permission_codes → permission IDs` using cached `formOptions`. Recomputes on every role change — **no extra API call**.

### When Management Role Changes

| Actor | Behavior |
|---|---|
| Superuser | `directPermIds` preset from new role's permissions |
| Platform Admin | `directPermIds` cleared — must re-add manually |

**Design decision:** Clearing direct perms on role change prevents stale assignments from carrying over to an unrelated role.

### Permission Checkbox Display

```typescript
checked  = rolePermIds.has(p.id) || directPermIds.includes(p.id)
disabled = rolePermIds.has(p.id)   // role perms: auto-checked, cannot be toggled
```

| Checkbox state | Source | Editable |
|---|---|---|
| Checked + greyed out | Role-derived (`rolePermIds`) | No |
| Checked + active | Direct (`directPermIds`) | Yes |
| Unchecked | Not assigned | Yes (if actor can assign direct perms) |

### On Save

```typescript
await updateUser({
  id: user.id,
  body: {
    first_name, last_name, email, is_active,
    department: deptId,
    roles: [...managementRoleId, ...systemRoleIds],
    permission_ids: directPermIds,   // direct perms only
  }
})
```

The backend re-derives all `SOURCE_ROLE` permissions from `roles` and stores `SOURCE_DIRECT` from `permission_ids`. No manual filtering needed on the frontend.
